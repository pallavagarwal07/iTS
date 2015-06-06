import globals


def process(code):
    var_str = globals.toplevelreplace(code, '\n', ' ')
    illegal_delimiters = ['"', "'", '(', ')', '[', ']']
    tokens = ''
    cur_tk = ''
    dbl_q = 0
    sing_q = 0
    paren = 0
    sq_brace = 0
    i = 0
    do_while = 0
    level = -1
    while i < len(var_str):
        ch = var_str[i]
        if ch not in illegal_delimiters:
            if sq_brace or paren or dbl_q or sing_q:
                cur_tk += ch
            elif ch in ['{', '}']:
                cur_tk += ('\n' + ch + '\n')
            elif ch == ';':
                cur_tk += (ch + '\n')
            elif var_str.startswith("if", i):
                level = paren
                i += 1
                cur_tk += "if"
            elif var_str.startswith("else", i):
                i += 3
                cur_tk += "else\n"
            elif var_str.startswith("for", i):
                level = paren
                i += 2
                cur_tk += "for"
            elif var_str.startswith("do", i):
                i += 1
                cur_tk += "do\n"
                do_while = 1
            elif var_str.startswith("while", i):
                if do_while == 0:
                    level = paren
                else:
                    do_while = 0
                i += 4
                cur_tk += "while"
            else:
                cur_tk += ch
        elif dbl_q:
            if ch=='"' and var_str[i-1]!='\\':
                dbl_q = 0
                cur_tk += ch
            else:
                cur_tk += ch
        elif sing_q:
            if ch=="'" and var_str[i-1]!='\\':
                sing_q = 0
                cur_tk += ch
            else:
                cur_tk += ch
        else:
            cur_tk += ch
            if ch == '(':
                paren += 1
            elif ch == ')':
                paren -= 1
                if level == paren:
                    level = -1
                    cur_tk += '\n'
            elif ch == '[':
                sq_brace += 1
            elif ch ==']':
                sq_brace -= 1
            elif ch == '"':
                dbl_q = 1
            elif ch == "'":
                sing_q = 1
        i += 1
    tokens += cur_tk
    return tokens
