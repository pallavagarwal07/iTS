def is_num(s):
    try:
        float(s)
        return eval(str(s))
    except ValueError:
        return 'Error'