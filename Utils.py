def match_brack(code, num):
    i = num
    start = 0
    for k in range(i, len(code)):
        line = code[k]
        if line == '{':
            start += 1
        if line == '}':
            start -= 1
        if start == 0:
            return k
    return i


def is_num(s):
    try:
        float(s)
        return eval(str(s))
    except ValueError:
        return 'Error'


def handle_num(s):
    try:
        float(s)
        return eval(str(s))
    except ValueError:
        return s