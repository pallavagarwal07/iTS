import sys
import globals
import PreProcessing
import Runtime

# inp variable stores user input.
globals.inp = sys.stdin.read()

# priority variable is a dictionary of operators and their priorities.
priority = globals.priority

# ops is a list of all operators.
ops = globals.ops

# CodeFile stores a reference to the c file that has to be parsed.
CodeFile = open('newTest.c')

# Preprocessor does some work here
code = PreProcessing.get_code(CodeFile)
code = PreProcessing.nest(code)

# Access is used to keep track of current scope
Access = ['global']

# Send the code to the execution factory
Runtime.execute(code, Access)
