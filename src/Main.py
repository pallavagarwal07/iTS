from globals import print1, print2, print3
import sys
import globals
import PreProcessing
import Runtime
import Exceptions
import stringDiff
#import Gui

print1("ARGS", sys.argv)

filename = sys.argv[1]

globals.vLevel = int(sys.argv[2]) # verbosity level

# inp variable stores user input.
if sys.argv[3] == 'stdin':
    globals.inp = sys.stdin.read()
else:
    globals.inp = open(sys.argv[3]).read()

# out variable is where c code's output is posted
if sys.argv[4] == 'stderr':
    globals.out = sys.stderr
else:
    globals.out = open(sys.argv[4], 'w')

# priority variable is a dictionary of operators and their priorities.
priority = globals.priority

# ops is a list of all operators.
ops = globals.ops

# CodeFile stores a reference to the c file that has to be parsed.
CodeFile = open(filename)

globals.raw_code = CodeFile.read()

# Preprocessor does some work here
code = PreProcessing.use_c_preprocessor(filename)

# Change all scope brackets and content into nested lists
code = PreProcessing.nest(code)
globals.code = code

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
    print3(e.message)
