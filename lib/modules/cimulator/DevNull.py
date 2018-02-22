# A /dev/null equivalent file pointer.

class DevNull:
    def close(self, *args):
        return

    def flush(self, *args):
        return

    def fileno(self, *args):
        return 0

    def isatty(self, *args):
        return False

    def next(self, *args):
        return self

    def read(self, *args):
        return ""

    def readline(self, *args):
        return ""

    def readlines(self, *args):
        return []

    def xreadlines(self, *args):
        return []
    
    def seek(self, *args):
        return

    def tell(self, *args):
        return 0

    def truncate(self, *args):
        return

    def write(self, *args):
        return

    def writelines(self, *args):
        return

