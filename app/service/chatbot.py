import logging
from app.util.predict_intent import IntentModel
from app.model.converstaion import Conversation, from_dict
from app.util.lexical_analyze import error_keyword_fix
from app.util.time import get_current_time
from app.util.answer import Answer
from app.util.predict_entity import EntityModel
from app.service import conversation as conversation_service


class ChatbotEngine:
    def __init__(self):
        self.intent_model = IntentModel()
        self.job_matching_entity_model = EntityModel('job_matching_entity.weight', 'job_matching_entity.params', 'job_matching_entity.preprocessor')
        self.conversation = None
        self.Answer = Answer()
        self.ans = None

    def process(self, message):
        """ 1. initialize or load conversation """
        self.conversation = from_dict(conversation_service.get_one({'sender': message.sender}))

        if self.conversation is None:
            # 최초로 수행한 사용자/chatroom에 대해서 Conversation 생성
            self.conversation = Conversation(sender=message.sender,
                                             message=message.message,
                                             status="0",
                                             last_time=get_current_time())
            conversation_service.insert_one(self.conversation.__dict__)
        else:
            # 현재 message의 sentTime과 마지막 채팅 시간과의 차이가 5분 미만일 경우 기존 상태를 채택한다.
            # 5분 이상일 경우 "0"상태로 conversation을 초기화 한다.
            # if message.sentTime - self.conversation.last_time >= 500000:
            #     self._to_status('0')

            self.conversation.last_time = get_current_time()
            self.conversation.message = message.message
            conversation_service.update_one(self.conversation.__dict__)

            logging.debug('[ Conversation with \'{0} ]'.format(self.conversation.sender))
        self.conversation.message = error_keyword_fix(self.conversation.message)

        """ 2. generate answer """
        # initialize
        self.ans = self.Answer.i_dont_know()

        # hot keys
        if self.conversation.message == "처음단계로" or self.conversation.message == "아니":
            self.ans = self.Answer.init_message()
            self._to_status('0')
            # self.btn[3] = True
        elif self.conversation.message == "안녕":
            self.ans = self.Answer.hello(self.conversation.sender)
            self._to_status('0')
            # self.btn[3] = True
        elif self.conversation.message == "도움말":
            self.ans = self.Answer.help()
            self._to_status('0')

        # general
        else:
            self._generate_answer()

        """ 3. teardown """
        # save conversation into database
        conversation_service.update_one(self.conversation.__dict__)
        logging.debug('status : ' + self.conversation.status)

        return self.ans

    def _generate_answer(self):
        if self.conversation.status == "0" or self.conversation.status == "4":
            """
                Initial Status
            """
            self._process_status_initial()

        elif self.conversation.status == "1":
            # 테스트 단계 설정 필요
            self.ans = self.Answer.employee_desired_salary()
            self.ans = '[희망급여]\n' + self.ans
            self._to_status('2')
        elif self.conversation.status == "2":
            # 테스트 단계 설정 필요
            self._to_status('0')
            if '그래' in self.conversation.message or '응' in self.conversation.message \
                    or '해줘' in self.conversation.message:
                self.ans = '[알바검색] 넵 바로 확인해보겠습니다.'
                # todo: 알바검색 프로세스 진행
            else:
                self.ans = self.Answer.init_message()

        elif self.conversation.status == "a":
            # 테스트 단계 설정 필요
            self.ans = self.Answer.employer_desired_salary()
            self._to_status('b')
        elif self.conversation.status == "b":
            self._to_status('0')
            if '그래' in self.conversation.message or '응' in self.conversation.message \
                    or '해줘' in self.conversation.message:
                self.ans = '[알바검색] 넵 바로 찾아보겠습니다.'

    def _process_status_initial(self):
        # 1. get intent
        intent = self.intent_model.predict(self.conversation.message)
        logging.debug('intent : ' + intent)

        if intent == "안녕":
            self.ans = self.Answer.hello(self.conversation.sender)
            self._to_status('0')

        elif intent == "알바구하기":
            self._searching_job_after_process()
            self.ans = '[알바구하기]\n' + self.ans

        else:
            # todo : ?
            logging.debug('바보야')

    def _searching_job_after_process(self):
        entities = self.job_matching_entity_model.predict(self.conversation.message)['entities']
        logging.debug('entities-->')
        logging.debug(entities)
        for entity in entities:
            if entity['type'] == 'job':
                self.conversation.job = entity['text']
            elif entity['type'] == 'type':
                self.conversation.type = entity['text']
        if self.conversation.sender == '편의점꿈나무':
            self.ans = self.Answer.employee_ask_require_date(self.conversation.job, self.conversation.type)
            self._to_status('1')
        else:
            if self.conversation.type == '바로' or self.conversation.type == '긴급':
                self.ans = '[긴급]건으로 희망일자는 전체가능으로 검색하겠습니다.\n'
                self.ans = self.ans + self.Answer.employer_desired_salary()
                self._to_status('b')
            else:
                self.ans = self.Answer.employer_ask_require_date(self.conversation.job, self.conversation.type)
                self._to_status('a')

    def _to_status(self, status):
        if status == '0':
            self.conversation.status = '0'
            self._initialize_info()
        else:
            self.conversation.status = status

    def _initialize_info(self):
        self.conversation.job = None
        self.conversation.type = None
