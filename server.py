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

    def serve(self):
        poller = select.poll()
        poller.register(self.server_socket, select.POLLIN)

        while True:
            events = poller.poll()
            for fd, event in events:
                if event & select.POLLNVAL:
                    self.connections.pop(fd)
                    poller.unregister(fd)
                    continue

                if fd == self.server_socket.fileno():
                    client_socket, _ = self.server_socket.accept()
                    connection = Connection(client_socket, self.dir)
                    self.connections[client_socket.fileno()] = connection
                    poller.register(client_socket, select.POLLIN)
                    continue

                connection = self.connections[fd]
                connection.handle()

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
