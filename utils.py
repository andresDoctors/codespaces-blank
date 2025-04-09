def parseNonNegativeInts(*args):
    nats = tuple(int(arg) for arg in args)
    if any(n < 0 for n in nats):
        raise ValueError()
    return nats


def read_file_slice(filepath, offset, slice_size):
    with open(filepath, 'rb') as f:
        f.seek(offset)
        return f.read(slice_size)
