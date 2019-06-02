class User:

    def __init__(self, user_id=None, name=None, status=None, last_time=None, last_message=None, testjob_id=None, history_num=None, chatroom_id=None):
        self.name = name
        self.user_id = user_id
        self.status = status
        self.last_time = last_time
        self.last_message = last_message
        self.testjob_id = testjob_id
        self.history_num = history_num
        self.chatroom_id = chatroom_id

    def __repr__(self):
        return '<User %r>' % (self.name)

    def from_dict(self, dict):
        if dict is None:
            return None

        self.__init__(dict['user_id'], dict['name'], dict['status'], dict['last_time'], dict['last_message'],
                      dict['testjob_id'], dict['history_num'], dict['chatroom_id'])
        return self
