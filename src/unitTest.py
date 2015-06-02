import sys
import globals
import PreProcessing
import Gui
import Runtime

def test(code, input, propOut, output):
    file = open("autoTest.c", 'w')
    file.write(code)
    file.close()

    filename = 'autoTest.c'

    # inp variable stores user input.
    globals.inp = input

    # priority variable is a dictionary of operators and their priorities.
    priority = globals.priority

    # ops is a list of all operators.
    ops = globals.ops

    # CodeFile stores a reference to the c file that has to be parsed.
    CodeFile = open(filename)

    # Preprocessor does some work here
    code = PreProcessing.use_c_preprocessor(filename)

    # code = PreProcessing.get_code(CodeFile)
    code = PreProcessing.nest(code)
    # Gui.make_ui(code)
    # print globals.type_range
    # Access is used to keep track of current scope
    Access = ['global']
    globals.setup()
    # Build a dictionary of functions and run main
    Runtime.traverse(code, Access)
