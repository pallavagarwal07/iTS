import re


def get_code(code_file):
    code_list = []
    code_buffer = []
    for line in code_file:
        line = line.replace('{', '\n{\n').replace('}', '\n}\n').replace(';', ';\n')
        if '//' in line:
            line.replace('//', '\n//')
        code_list.append(line)
        code_buffer = []
        for item in code_list:
            code_buffer += item.split('\n')
    str1 = ''
    for line in code_buffer:
        line = " ".join(line.split())
        if len(line.split()) < 1:
            continue
        if '//' in line:
            continue
        str1 += (line + '\n')
    str1 = re.sub(r'(?s)/\*.*?\*/', '', str1)
    str1 = str1.split('\n')
    code_buffer = []
    for line in str1:
        code_buffer.append(line.strip())
    return code_buffer


def nest(code):
    bracks = []
    i = 0
    while i < len(code):
        if code[i] == '{':
            bracks.append(i)
        elif code[i] == '}':
            match = bracks.pop()
            code = code[:match] + [code[match + 1:i]] + code[i + 1:]
            i = match + 1
        i += 1
    return code

