from constants import (BAD_EOL, BAD_REQUEST, EOL, INTERNAL_ERROR)
from command_handler import CommandHandler
from response import Response


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
        disconnect = False

        try:
            request = self.receive()
            response = self.process_request(request)
            self.respond(response)
            disconnect = response.disconnect
        except (RecvException, SendallException, ConnectionClosedByPeer):
            disconnect = True
        except BufferOverflow:
            response = Response(BAD_REQUEST)
            self.respond(response)
            disconnect = True
        except Exception as e:
            response = Response(INTERNAL_ERROR, str(e))
            self.respond(response)
            disconnect = True
        finally:
            return disconnect


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

    def respond(self, response):
        message = f'{response.code} {response.body}{EOL}'
        message = message.encode('ascii')

        try:
            self.client_socket.sendall(message)
        except Exception as e:
            raise SendallException() from e

    def process_request(self, request):
        if '\n' in request:
            return Response(BAD_EOL)

        cmd, *args = request.split()
        return self.command_handler(cmd, *args)
