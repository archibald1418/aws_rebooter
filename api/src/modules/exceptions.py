class NotAuthorized(Exception):
    def __init__(self):
        self.message = 'You are not regisered to use this bot'
        super().__init__(self.message)

class Forbidden(Exception):
    def __init__(self):
        self.message = "You are not allowed to invoke this command"
        super().__init__(self.message)