from command_handler import (CommandHandler, QuitRequest)
from response import Response
from protocol import EOL, BAD_EOL, CODE_OK, BAD_REQUEST, INTERNAL_ERROR


class ConnectionClosedByPeer(Exception):
    pass


class BufferOverflow(Exception):
    pass


class RecvException(Exception):
    pass


class SendallException(Exception):
    pass


class Connection:
    MAX_BUFFER_SIZE = 256 * 2**20

    def __init__(self, client_socket, directory):
        self.client_socket = client_socket
        self.command_handler = CommandHandler(directory)
        self.buffer = ''

    def handle(self):
        try:
            #while True:
            request = self.receive()
            response = self.process_request(request)
            self.respond(response)
        except Exception as e:
            self.respond_on_exception(e)
            self.client_socket.close()

    def receive(self):
        while EOL not in self.buffer:
            try:
                chunk = self.client_socket.recv(1024)
            except Exception as e:
                raise RecvException() from e

            chunk = chunk.decode('ascii')
            if chunk == '':
                raise ConnectionClosedByPeer()
            if len(self.buffer) + len(chunk) > Connection.MAX_BUFFER_SIZE:
                raise BufferOverflow()

            self.buffer += chunk

        i = self.buffer.find(EOL)
        request = self.buffer[:i]
        self.buffer = self.buffer[i + len(EOL):]

        return request

    def process_request(self, request):
        if '\n' in request:
            return Response(BAD_EOL)

        cmd, *args = request.split()
        return self.command_handler(cmd, *args)

    def respond(self, response):
        message = f'{response.code} {response.body}{EOL}'
        message = message.encode('ascii')

        try:
            self.client_socket.sendall(message)
        except Exception as e:
            raise SendallException() from e

    def respond_on_exception(self, e):
        RESPONSE_CODES = {
            RecvException: None,
            SendallException: None,
            ConnectionClosedByPeer: None,
            BufferOverflow: BAD_REQUEST,
            QuitRequest: CODE_OK
        }

        code = RESPONSE_CODES.get(type(e), INTERNAL_ERROR)
        if code is not None:
            response = Response(code)
            self.respond(response)
