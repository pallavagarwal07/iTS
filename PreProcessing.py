import re
import os
from subprocess import PIPE, Popen, check_output


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


def use_c_preprocessor(filename):
    content = os.popen('gcc -E ' + filename)
    content = list(content.readlines())
    code = []
    flag = False
    for line in content:
        if flag and not line.startswith('#'):
            code.append(line)
        elif line.startswith('#'):
            if filename in line:
                flag = True
            else:
                flag = False
    code = "\n".join(code)
    a = Popen(['echo', code], stdout=PIPE)
    a = Popen(
        ['indent', '-nhnl', '-nbc', '-nce', '-sob', '-nlps', '-i0', '-cli0', '-bli0', '-bls', '-npcs'], stdin=a.stdout,
        stdout=PIPE)
    code = a.stdout.read().split('\n')
    code = [line.strip() for line in code]
    content = []
    for line in code:
        if len(line) > 0:
            content.append(line)
    return content


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

