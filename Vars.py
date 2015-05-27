import globals


def get_val(key):
    if type(key) is not tuple:
        return key
    else:
        if len(key) != 1:
            t = globals.in_var_table(key[0], key[1])
            if t:
                return globals.var_table[t][0].v
        else:
            if key in globals.memory:
                return globals.memory[key][0].v
            else:
                print "Invalid Memory location get_val"
                exit(0)


def set_val(key, val):
    if len(key) != 1:
        t = globals.in_var_table(key[0], key[1])
        if t:
            globals.var_table[t][0].v = val
    else:
        if key in globals.memory:
            print "setting ", val, "to ", key
            globals.memory[key][0].v = val
        else:
            print "Invalid Memory location set_val", key
            exit(0)
