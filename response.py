CODE_OK = 0
BAD_EOL = 100
BAD_REQUEST = 101
INTERNAL_ERROR = 199
INVALID_COMMAND = 200
INVALID_ARGUMENTS = 201
FILE_NOT_FOUND = 202
BAD_OFFSET = 203

error_messages = {
    CODE_OK: "OK",
    BAD_EOL: "BAD EOL",
    BAD_REQUEST: "BAD REQUEST",
    INTERNAL_ERROR: "INTERNAL SERVER ERROR",
    INVALID_COMMAND: "NO SUCH COMMAND",
    INVALID_ARGUMENTS: "INVALID ARGUMENTS FOR COMMAND",
    FILE_NOT_FOUND: "FILE NOT FOUND",
    BAD_OFFSET: "OFFSET EXCEEDS FILE SIZE",
}

EOL = '\r\n'

class ConnectionClosedByPeer(Exception):
    pass


class BufferOverflow(Exception):
    pass


class RecvException(Exception):
    pass


class SendallException(Exception):
    pass


class QuitRequest(Exception):
    pass


class Response:
    def __init__(self, code, body=None):
        self.code = code
        self.body = body

        if self.body is None:
            self.body = error_messages[code]
