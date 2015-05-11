import globals


def get_val(key):
    print "Get Val got key " + str(key)
    return globals.var_table[key][0]


def set_val(key, val):
    globals.var_table[key][0] = val
