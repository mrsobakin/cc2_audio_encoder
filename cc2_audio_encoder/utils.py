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
        except:
            pass
        try:
            os.rmdir(tmpdir)  # Remove directory
        except:
            pass
