# Behaves like Main, but doesn't invoke the filesystem. Written to
# test with pypyjs.
from __future__ import print_function, absolute_import
try:
    from StringIO import StringIO
except Exception as e:
    from io import StringIO

from .Globals import print1, print2, print3
from .Globals import b64encode as b64
from . import Globals
from . import PreProcessing
from . import Runtime
from . import Exceptions
from . import StringDiff

def start(stdin, stdout, cmdout, code, verbosity=0):
    Globals.inp      = stdin.read()
    Globals.out      = stdout
    Globals.vLevel   = verbosity
    Globals.cmd      = cmdout
    Globals.raw_code = code.read()

    # Preprocessor does some work here like resolve define
    # statements and removing include statements and comments.
    code = PreProcessing.use_c_preprocessor()

    # Change all scope brackets and content into nested lists
    code = PreProcessing.nest(code)
    Globals.code = code

    # String difference found in the beginning is used to find
    # the current executing line during execution.
    StringDiff.init(str(Globals.code), str(Globals.raw_code))

    Globals.setup()

    print1(code)

    # Build a dictionary of functions and run main
    try:
        Runtime.traverse(code, 'global')

    except Exceptions.main_executed as e:
        Globals.cmd.write(str(e) + "\ndelete_scope('global');")

    except Exceptions.any_user_error as e:
        print("e is ", e, type(e))
        Globals.cmd.write(Globals.gui + \
                "\nuser_error('{0}');".format(b64(' '.join(e.args))))

def sample_run():
    inp = make_file("42\n")
    out = StringIO()
    cmd = StringIO()
    src = make_file(r"""
    #include <stdio.h>
    #define s(num) scanf("%d", &num)
    #define p(num) printf("%d\n", num)

    int main() {
        int a;
        s(a);
        printf("Answer to life is: ");
        p(a);
        return 0;
    }""")

    start(inp, out, cmd, src)
    print("------")
    out.seek(0)
    print(out.read())
    print("------")
    cmd.seek(0)
    print(cmd.read())
    print("------")

def make_file(content):
    f = StringIO()
    f.write(content)
    f.seek(0)
    return f
