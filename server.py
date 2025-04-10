import socket
from connection import Connection
import argparse
import select

DEFAULT_DIR = 'testdata'
DEFAULT_ADDR = '0.0.0.0'
DEFAULT_PORT = 19500

class Server(object):

    def __init__(self, address, port, directory):
        self.addr = address
        self.port = port
        self.dir = directory

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.addr, self.port))
        self.server_socket.listen()

        self.connections = {}
        self.poller = select.poll()
        self.poller.register(self.server_socket, select.POLLIN)

    def serve(self):
        while True:
            events = self.poller.poll()
            for fd, event in events:
                if fd == self.server_socket.fileno():
                    self.handle_server_socket(event)
                elif fd in self.connections:
                    self.handle_client_socket(fd, event)

    def handle_server_socket(self, event):
        SERVER_SOCKET_HANDLERS = {
            select.POLLIN: self.accept_client,
        }

        for bitmask, handler in SERVER_SOCKET_HANDLERS.items():
            if event & bitmask:
                handler()
    
    def handle_client_socket(self, fd, event):
        connection = self.connections[fd]
        CLIENT_SOCKET_HANDLERS = {
            select.POLLIN: connection.handle,
            select.POLLNVAL: (lambda: self.remove_connection(fd)),
        }

        for bitmask, handler in CLIENT_SOCKET_HANDLERS.items():
            if event & bitmask:
                handler()

    def accept_client(self):
        client_socket, _ = self.server_socket.accept()
        connection = Connection(client_socket, self.dir)
        self.connections[client_socket.fileno()] = connection
        self.poller.register(client_socket, select.POLLIN)

    def remove_connection(self, fd):
        self.connections.pop(fd)
        self.poller.unregister(fd)


def parse_input():
    parser = argparse.ArgumentParser()

    default, help = DEFAULT_ADDR, f'default:{DEFAULT_ADDR}'
    parser.add_argument('-a', '--address', default=default, help=help)

    default, help = DEFAULT_PORT, f'default:{DEFAULT_PORT}'
    parser.add_argument('-p', '--port', default=default, help=help, type=int)

    default, help = DEFAULT_DIR, f'default:{DEFAULT_DIR}'
    parser.add_argument('-d', '--directory', default=default, help=help)

    args = parser.parse_args()
    return args.address, args.port, args.directory

if __name__ == '__main__':
    address, port, directory = parse_input()
    server = Server(address, port, directory)
    server.serve()
