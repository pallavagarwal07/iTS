from .Globals import print1, print2, print3
from . import Globals
from . import PreProcessing
from . import Gui
from . import Runtime

def test(code, input, propOut, output):
    file = open("autoTest.c", 'w')
    file.write(code)
    file.close()

    filename = 'autoTest.c'

    # inp variable stores user input.
    Globals.inp = input

    # priority variable is a dictionary of operators and their priorities.
    priority = Globals.priority

    # ops is a list of all operators.
    ops = Globals.ops

    # CodeFile stores a reference to the c file that has to be parsed.
    CodeFile = open(filename)

    # Preprocessor does some work here
    code = PreProcessing.use_c_preprocessor(filename)

    # code = PreProcessing.get_code(CodeFile)
    code = PreProcessing.nest(code)
    # Gui.make_ui(code)
    # Access is used to keep track of current scope
    Access = ['global']
    Globals.setup()
    # Build a dictionary of functions and run main
    Runtime.traverse(code, Access)
