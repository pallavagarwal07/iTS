# Behaves like Main, but doesn't invoke the filesystem. Written to
# test with pypyjs.
from __future__ import print_function, absolute_import

from .Globals import print1, print2, print3
from .Globals import b64encode as b64
from . import Globals
from . import PreProcessing
from . import Runtime
from . import Exceptions
from . import StringDiff
try:
    from StringIO import StringIO
except Exception as e:
    from io import StringIO


Globals.vLevel = 0
Globals.inp = "56\n"

Globals.out = StringIO()
cmd = StringIO()

Globals.raw_code = r"""
int main() {
    int a;
    scanf("%d", &a);
    printf("%d\n", a);
    return 0;
}
"""

# Preprocessor does some work here like resolve define statements
# and removing include statements and comments.
code = PreProcessing.use_c_preprocessor()

# Change all scope brackets and content into nested lists
code = PreProcessing.nest(code)
Globals.code = code

# String difference found in the beginning is used to find the current
# executing line during execution.
StringDiff.init(str(Globals.code), str(Globals.raw_code))

#Gui.make_ui(code)

# Access is used to keep track of current scope
Access = 'global'

Globals.setup()

print1(code)

# Build a dictionary of functions and run main
try:
    Runtime.traverse(code, Access)
except Exceptions.main_executed as e:
    cmd.write(str(e) + "\ndelete_scope('global');")
except Exceptions.timeout_error:
    msg = "Your program timed out at this position. If this happened at an array" + \
            "declaration, declare a smaller array, and try again. Otherwise, try" + \
            "the program with smaller inputs."
    cmd.write(Globals.gui + "\nuser_error('{0}');".format(b64(msg)))
except Exceptions.any_user_error as e:
    print("e is ", e, type(e))
    cmd.write(Globals.gui + "\nuser_error('{0}');".format(b64(' '.join(e.args))))
finally:
    Globals.out.seek(0)
    print("------")
    print(Globals.out.read())
