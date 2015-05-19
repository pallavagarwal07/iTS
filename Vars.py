import globals


def get_val(key):
    if type(key) is not tuple:
        return key
    else:
        t = globals.in_var_table(key[0], key[1])
        if t:
            return globals.var_table[t][0]


def set_val(key, val):
    t = globals.in_var_table(key[0], key[1])
    if t:
        globals.var_table[t][0] = val
