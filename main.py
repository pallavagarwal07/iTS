from __future__ import print_function
import signal
import sys

import cimulator

class timeout_error(Exception):
    pass

def timeout(signum, frame):
    raise timeout_error("TIME UP!")

signal.signal(signal.SIGALRM, timeout)
signal.alarm(10000)

filesource = open(sys.argv[1])
verbosity  = int(sys.argv[2])

# inp variable stores user input.
if sys.argv[3] == 'stdin':
    stdin = sys.stdin
else:
    stdin = open(sys.argv[3])

# out variable is where c code's output is posted
if sys.argv[4] == 'stdout':
    stdout = sys.stderr
else:
    stdout = open(sys.argv[4], 'w')

if sys.argv[5] == 'stderr':
    cmd = sys.stderr
else:
    cmd = open(sys.argv[5], 'w')

# Build a dictionary of functions and run main
try:
    cimulator.start(stdin, stdout, cmd, filesource, verbosity)

except timeout_error:
    msg = "Your program timed out at this position."     + \
            " If this happened at an array declaration," + \
            " declare a smaller array, and try again."   + \
            " Otherwise, try the program with smaller"   + \
            " inputs."
    cmd.write(Globals.gui + \
            "\nuser_error('{0}');".format(b64(msg)))
