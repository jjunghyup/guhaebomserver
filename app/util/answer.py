import random

class Answer(object):
    def __init__(self):
        self.LANG = 'KO'

    # inform #
    def hello(self, sender_name):
        if self.LANG is 'KO':
            ans = '안녕하세요. ' + sender_name + '님 \n' \
                  '무엇을 도와드릴까요?'

        return ans

    def to_init(self):
        if self.LANG is 'KO':
            ans = '\n\n상태를 자동으로 "처음단계로" 전환합니다.\n' \
                   '무엇을 도와드릴까요?'
        return ans

    def init_message(self):
        if self.LANG is 'KO':
            ans = '"처음단계로" 전환합니다.\n' \
                   '무엇을 도와드릴까요?'

        return ans

    def help(self):
        if self.LANG is 'KO':
            ans =  '안녕하세요? 구해봄 봇 도움말입니다.\n' \
                   '저는 다음과 같은 업무를 도와드릴 수 있습니다.\n' \
                   '1. 일자리 구하기\n' \
                   '   > 일자리 구하고 싶어\n' \
                   '2. 무언가\n' \
                   '   > 무언가\n'
        return ans

    def i_dont_know(self):
        if self.LANG is 'KO':
            ans = '죄송합니다. 무슨 말씀인지 모르겠어요.'

        return ans

    def i_dont_do(self):
        if self.LANG is 'KO':
            ans = '해당 기능은 지원하지 않습니다.'

        return ans

    def employee_ask_require_date(self, job=None, type=None):
        if self.LANG is 'KO':
            ans = ''
            if type is not None:
                ans = ans + ' [' + type + ']으로 진행하겠습니다.\n'
            if job is not None:
                ans = ans + ' - 일자리 : ' + job + '\n'
            ans = ans + ' 구인을 원하는 정확한 시간을 알 수 있을까요?\n[달력]'
            return ans

    def employer_ask_require_date(self, job=None, type=None):
        if self.LANG is 'KO':
            ans = ''
            if type is not None:
                ans = ans + ' [' + type + ']으로 진행하겠습니다.\n'
            if job is not None:
                ans = ans + ' - 일자리 : ' + job + '\n'
            ans = ans + ' 구직을 원하는 정확한 시간을 알 수 있을까요?\n[달력]'
            return ans

    def employee_desired_salary(self):
        if self.LANG is 'KO':
            ans = '희망시급은 기존과 동일한 10,000원으로 하겠습니다.'
            return ans

    def employer_desired_salary(self):
        if self.LANG is 'KO':
            ans = '급여는 기존에 입력하신 10,000원으로 알아볼까요?'
            return ans

    def error(self):
        """
            알 수 없는 오류
        """
        if self.LANG is 'KO':
            ans = '알 수 없는 오류가 발생했습니다.\n'
            ans += 'Testopia 관리자에게 문의하세요.'

        return ans + self.to_init()

    # etc #

    def easter_egg(self):
        msg = ['난 멍청이야 @_@ 너무 많은 것을 묻지 말아줘..',
               '난 심심이가 아니야 ㅠㅠ',
               '사실 챗봇 아님 걍 if-else임',
               '내가 위대한 테스토피아다!',
               '앙용하세용 뿌잉뿌잉',
               '뿌우? 테뜨또삐아 와쪄염 뿌우',
               '제가 쓴거 아님다. 지나가던 고양이가 썼어요.',
               '나는 우면에 사는 테스토피아!',
               '어피치짱']
        return random.choice(msg)

