
class AuthException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NotAuthorized(AuthException):
    def __init__(self):
        self.message = 'You are not regisered to use this bot'
        super().__init__(self.message)

class Forbidden(AuthException):
    def __init__(self):
        self.message = "You are not allowed to invoke this command"
        super().__init__(self.message)