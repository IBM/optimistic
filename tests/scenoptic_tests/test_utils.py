import sys
import traceback
from pathlib import Path

test_root_dir = Path.resolve(Path.joinpath(Path(__file__), '../../..'))


class Tee(object):
    def __init__(self, filename):
        self.file = open(filename, mode='w', encoding='utf8')
        self.stdout = sys.stdout

    def __enter__(self):
        sys.stdout = self

    def __exit__(self, exc_type, exc_value, tb):
        sys.stdout = self.stdout
        if exc_type is not None:
            self.file.write(traceback.format_exc())
        self.file.close()

    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)

    def flush(self):
        self.file.flush()
        self.stdout.flush()
