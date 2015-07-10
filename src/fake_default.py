import re
import globals
import Exceptions

def invoke(name, params, scope):
    if name == 'sizeof':
        if len(params) != 1:
            raise Exceptions.any_user_error("Incorrect number of parameters.")
        t = re.findall(r'\*', params[0])
        if t:
            return globals.sizeof['pointer']
        else:
            return globals.sizeof[params[0].strip()]
    if name == 'malloc':
        raise Exceptions.any_user_error("Malloc hasn't been implemented yet.")
