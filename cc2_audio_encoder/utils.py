import os
import tempfile
from contextlib import contextmanager


@contextmanager
def temp_file():
    tmpdir = tempfile.mkdtemp()
    filename = os.path.join(tmpdir, 'temp')  # Temporary filename
    try:
        yield filename
    finally:
        try:
            os.remove(filename)  # Remove file
        except Exception:
            pass

        try:
            os.rmdir(tmpdir)  # Remove directory
        except Exception:
            pass


def interleave(iter1, iter2):
    for a, b in zip(iter1, iter2):
        yield a
        yield b


# https://stackoverflow.com/a/312464
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def to2B(n):
    return n.to_bytes(2, byteorder="big")


def to4B(n):
    return n.to_bytes(4, byteorder="big")
