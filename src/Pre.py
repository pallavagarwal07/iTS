from globals import print1, print2, print3
import globals


def remove_non_string_newlines(code):
    code = list(code)
    dblq = 0
    sngq = 0
    for i, char in enumerate(code):
        if char == '"' and code[i-1] != '\\' and not sngq:
            dblq = 1 - dblq
        elif char == "'" and code[i-1] != '\\' and not dblq:
            sngq = 1 - sngq
        elif not sngq and not dblq and char == '\n':
            code[i] = ' '

    for i, char in enumerate(code):
        if char == '"' and code[i-1] != '\\' and not sngq:
            dblq = 1 - dblq
        elif char == "'" and code[i-1] != '\\' and not dblq:
            sngq = 1 - sngq
        elif not sngq and not dblq and char == ' ':
            j = i + 1
            while j < len(code) and ( code[j] == ' ' or code[j] == '\t' ):
                code[j] = ''
                j += 1
    return ''.join(code)


def process(code):
    var_str = remove_non_string_newlines(code)
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
    ques = 0
    while i < len(var_str):
        ch = var_str[i]
        if ch not in illegal_delimiters:
            if sq_brace or paren or dbl_q or sing_q:
                cur_tk += ch
            elif ch in ['{', '}']:
                temp = i-1
                while var_str[temp] in [' ', '\t']:
                    temp -= 1
                if var_str[temp] != '=':
                    cur_tk += ('\n' + ch + '\n')
                else:
                    array_brace = 1
                    while array_brace:
                        if var_str[i] is not '\n' or var_str[i] is not ' ':
                            cur_tk += var_str[i]
                        i += 1
                        if var_str[i] is '{':
                            array_brace += 1
                        elif var_str[i] is '}':
                            array_brace -= 1
                    cur_tk += var_str[i]
            elif ch == ';':
                cur_tk += (ch + '\n')
            elif var_str.startswith("case", i):
                cur_tk += "case"
                j = i + 4
                flag = 1
                while flag:
                    cur_tk += var_str[j]
                    if var_str[j] == '?':
                        ques += 1
                    elif var_str[j] == ':':
                        if ques:
                            ques -= 1
                        else:
                            cur_tk += '\n'
                            flag = 0
                    j += 1
                i = j
            elif var_str.startswith("default", i):
                cur_tk += "default :\n"
                while var_str[i] is not ':':
                    i += 1
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
            elif var_str.startswith("switch", i):
                level = paren
                i += 5
                cur_tk += "switch"
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
    print1(tokens)
    return tokens
