import os
import utils
from base64 import b64encode
from response import (Response, QuitRequest, INVALID_COMMAND, INVALID_ARGUMENTS, CODE_OK, FILE_NOT_FOUND, EOL, BAD_OFFSET)


class CommandHandler:

    def __init__(self, directory):
        self.directory = directory
        self.commands = {
            'get_file_listing': (self.get_file_listing, 0),
            'get_metadata': (self.get_metadata, 1),
            'get_slice': (self.get_slice, 3),
            'quit': (self.quit, 0),
        }

    def __call__(self, cmd, *args):
        if cmd not in self.commands:
            return Response(INVALID_COMMAND)

        command, param_count = self.commands[cmd]
        if len(args) != param_count:
            return Response(INVALID_ARGUMENTS)

        return command(*args)

    def get_file_listing(self):
        filenames = os.listdir(self.directory)
        lines = ['OK'] + filenames + ['']
        return Response(CODE_OK, EOL.join(lines))

    def get_metadata(self, filename):
        filepath = os.path.join(self.directory, filename)
        if not os.path.exists(filepath):
            return Response(FILE_NOT_FOUND)

        size = os.path.getsize(filepath)
        return Response(CODE_OK, f'OK{EOL}{size}')

    def get_slice(self, filename, offset, slice_size):
        try:
            offset, slice_size = utils.parseNonNegativeInts(offset, slice_size)
            filepath = os.path.join(self.directory, filename)
            file_size = os.path.getsize(filepath)
        except ValueError:
            return Response(INVALID_ARGUMENTS)
        except FileNotFoundError:
            return Response(FILE_NOT_FOUND)

        if offset + slice_size > file_size:
            return Response(BAD_OFFSET)

        slice = utils.read_file_slice(filepath, offset, slice_size)
        slice = b64encode(slice)
        slice = slice.decode('ascii')

        return Response(CODE_OK, f'OK{EOL}{slice}')

    def quit(self):
        raise QuitRequest()
