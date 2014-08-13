# #
# # This file is placed under the public domain.
# #
"""Utility functions for the tests."""
import os
import sys

PY3K = sys.version_info[0] == 3

class StreamOutput(object):
    def __init__(self, stream):
        self.stream = stream
        try:
            self.startoffset = self.stream.tell()
        except IOError:
            self.startoffset = 0
        self.curoffset = 0

    def writeline(self, data=None):
        if data:
            self.stream.write(data)
        self.stream.write(os.linesep)
        if data:
            self.curoffset = len(data)
        else:
            self.curoffset = 0
        self.stream.flush()

    def write(self, data):
        self.stream.write(data)
        self.curoffset = len(data)
        self.stream.flush()

    def writesame(self, data):
        overhang = self.curoffset - len(data)
        if overhang > 0:
            self.stream.write("%s %s\r" % (data, " " * overhang))
        else:
            self.stream.write("%s\r" % data)
        self.curoffset = len(data)
        self.stream.flush()

class TeeOutput(object):
    def __init__(self, stream1, stream2):
        self.outputs = [stream1, stream2]

    # -- methods from sys.stdout / sys.stderr
    def write(self, data):
        for stream in self.outputs:
            if PY3K:
                if 'b' in stream.mode:
                    data = data.encode('utf-8')
            stream.write(data)

    def tell(self):
        raise IOError

    def flush(self):
        for stream in self.outputs:
            stream.flush()
    # --/ sys.stdout
