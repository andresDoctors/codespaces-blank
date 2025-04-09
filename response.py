from constants import (error_messages, fatal_status)

class Response:
    def __init__(self, code, body=None, disconnect=None):
        self.code = code
        self.body = body
        self.disconnect = disconnect
    
        if self.body is None:
            self.body = error_messages[code]
        if self.disconnect is None:
            self.disconnect = fatal_status(code)