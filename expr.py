from tabulate import tabulate
import re
import sys
    
def isUpdation(exp, scope):
    k = re.match(r'^(?s)\s*[a-zA-Z_]+[a-zA-Z0-9_]*\s*=.*;', exp)
    return (1 if k else 0)

