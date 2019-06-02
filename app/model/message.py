class Message:

    def __init__(self, sender=None, message=None):
        self.sender = sender
        self.message = message

    def __repr__(self):
        return '<User %r %r %r>' % (self.sender, self.message)
