class Conversation:

    def __init__(self, sender=None, message=None, status=None, last_time=None, infodata=None, job = None, type = None):
        self.sender = sender
        self.message = message
        self.status = status
        self.last_time = last_time
        self.infodata = infodata
        self.job = job
        self.type = type

    def __repr__(self):
        return '<User %r>' % (self.sender)


def from_dict(dict):
    if dict is None:
        return None
    return Conversation(dict['sender'], dict['message'], dict['status'], dict['last_time'])
