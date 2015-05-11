import globals


def get_val(key):
    return globals.var_table[key][0]


def set_val(key, val):
    globals.var_table[key][0] = val
