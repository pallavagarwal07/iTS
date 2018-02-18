from globals import print1, print2, print3
from base64 import b64encode as b64
import signal
import sys
import globals
import PreProcessing
import Runtime
import Exceptions
import stringDiff


def timeout(signum, frame):
    raise Exceptions.timeout_error("TIME UP!")

signal.signal(signal.SIGALRM, timeout)
signal.alarm(10000)

print1("ARGS", sys.argv)

filename = sys.argv[1]

globals.vLevel = int(sys.argv[2]) # verbosity level

# inp variable stores user input.
if sys.argv[3] == 'stdin':
    globals.inp = sys.stdin.read()
else:
    globals.inp = open(sys.argv[3]).read()

# out variable is where c code's output is posted
if sys.argv[4] == 'stdout':
    globals.out = sys.stderr
else:
    globals.out = open(sys.argv[4], 'w')

if sys.argv[5] == 'stderr':
    cmd = sys.stderr
else:
    cmd = open(sys.argv[5], 'w')

# priority variable is a dictionary of operators and their priorities.
priority = globals.priority

# ops is a list of all operators.
ops = globals.ops

# CodeFile stores a reference to the c file that has to be parsed.
CodeFile = open(filename)

globals.raw_code = CodeFile.read()

# Preprocessor does some work here like resolve define statements
# and removing include statements and comments.
code = PreProcessing.use_c_preprocessor(filename)

# Change all scope brackets and content into nested lists
code = PreProcessing.nest(code)
globals.code = code

# String difference found in the beginning is used to find the current
# executing line during execution.
stringDiff.init(str(globals.code), str(globals.raw_code))

#Gui.make_ui(code)

# Access is used to keep track of current scope
Access = 'global'

globals.setup()

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
    cmd.write(globals.gui + "\nuser_error('{0}');".format(b64(msg)))
except Exceptions.any_user_error as e:
    print("e is ", e, type(e))
    cmd.write(globals.gui + "\nuser_error('{0}');".format(b64(bytes(' '.join(e.args), "UTF-8"))))
