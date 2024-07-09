import os
from logging import FileHandler

class OverwriteFileHandler(FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=False, maxBytes=0, backupCount=0):
        if mode == 'w':
            if os.path.isfile(filename):
                open(filename, 'w').close()  # Truncate the file if it exists
        super().__init__(filename, mode, encoding, delay)
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        if maxBytes > 0:
            self.mode = 'w'

    def emit(self, record):
        if self.shouldRollover(record):
            self.rollOver()
        super().emit(record)

    def shouldRollover(self, record):
        if self.maxBytes > 0:
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return True
        return False

    def rollOver(self):
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = "%s.%d" % (self.baseFilename, i)
                dfn = "%s.%d" % (self.baseFilename, i + 1)
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.baseFilename + ".1"
            if os.path.exists(dfn):
                os.remove(dfn)
            os.rename(self.baseFilename, dfn)
        if self.mode == 'w':
            self.stream.seek(0, 2)
        self.mode = 'w'
        self.stream.truncate()
        self.stream.seek(0, 0)