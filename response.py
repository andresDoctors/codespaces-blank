from protocol import (CODE_OK, BAD_EOL, BAD_REQUEST, INTERNAL_ERROR, INVALID_COMMAND, INVALID_ARGUMENTS, FILE_NOT_FOUND, BAD_OFFSET)

class Response:
    ERROR_MESSAGES = {
        CODE_OK: "OK",
        BAD_EOL: "BAD EOL",
        BAD_REQUEST: "BAD REQUEST",
        INTERNAL_ERROR: "INTERNAL SERVER ERROR",
        INVALID_COMMAND: "NO SUCH COMMAND",
        INVALID_ARGUMENTS: "INVALID ARGUMENTS FOR COMMAND",
        FILE_NOT_FOUND: "FILE NOT FOUND",
        BAD_OFFSET: "OFFSET EXCEEDS FILE SIZE",
    }

    def __init__(self, code, body=None):
        self.code = code
        self.body = body

        if self.body is None:
            self.body = Response.ERROR_MESSAGES[code]
