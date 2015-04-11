import re
import os
from subprocess import PIPE, Popen


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
        ['indent', '-nhnl', '-nbc', '-nce', '-sob', '-nlps', '-i0', '-cli0', '-bli0', '-bls', '-npcs'],
        stdin=a.stdout, stdout=PIPE)
    code = a.stdout.read()
    code = re.sub(r'else\s*if', 'else\nif', code)
    code = code.split('\n')
    code = [line.strip() for line in code]
    content = []
    for line in code:
        if len(line) > 0:
            content.append(line)
    print content
    return content


def group_if(code, n):
    print "Group if got: ", code, n
    i = n + 1
    line = code[i]
    if type(line) is str:
        k = re.findall(r'^(?s)if\s*\((.*)\)', line)
    else:
        if type(line) is list:
            code[i] = nest_conditionals(line)
        k = False
    if k:
        code = group_if(code, i)
    i += 1
    if i >= len(code) or code[i].strip() != 'else':
        code = code[:n] + [code[n:n + 2]] + code[n + 2:]
    else:
        i += 1
        line = code[i]
        if type(line) is str:
            k = re.findall(r'^(?s)if\s*\((.*)\)', line)
        else:
            k = False
        if k:
            code = group_if(code, i)
        code = code[:n] + [code[n:n + 4]] + code[n + 4:]
    print 'group if returned :', code, n
    return code


def nest_conditionals(code):
    i = 0
    while i < len(code):
        line = code[i]
        if type(line) is list:
            code[i] = nest_conditionals(line)
        else:
            k = re.findall(r'^(?s)if\s*\(.+\)', line)
            if k:
                code = group_if(code, i)
        i += 1
    return code


def nest(code):
    bracks = []
    i = 0
    while i < len(code):
        if code[i] == '{':
            bracks.append(i)
        elif code[i] == '}':
            print bracks
            match = bracks.pop()
            code = code[:match] + [code[match + 1:i]] + code[i + 1:]
            i = match
        i += 1
    print code
    code = nest_conditionals(code)

    return code
