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
    content = open(filename).read()
    content = os.popen('gcc -E ' + filename)
    content = content.readlines()
    content = list(content)
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
    a = Popen(['sed', '-r', r":a;N;$!ba;s/\s+/ /g"], stdin=a.stdout, stdout=PIPE)
    a = Popen(['sed', r's:}:}\n:'], stdin=a.stdout, stdout=PIPE)
    a = Popen(['astyle', '-A10', '-k3'], stdin=a.stdout, stdout=PIPE)
    a = Popen(['astyle', '--indent=spaces', '-A1', '-e'], stdin=a.stdout, stdout=PIPE)
    a = Popen(['sed', '-r', r"s/^\s*//"], stdin=a.stdout, stdout=PIPE)
    a = Popen(['sed', '-r', r"s/\s*$//"], stdin=a.stdout, stdout=PIPE)
    code = a.stdout.read()
    code = code.split('\n')
    code = [line.strip() for line in code]
    content = []
    for line in code:
        if len(line) > 0:
            content.append(line)
    return content


def nest_groups(code, i, make_list):
    while i < len(code):
        line = code[i]
        if type(line) is list:
            code[i] = nest_groups(line, 0, 0)
            if make_list:
                return code
        else:
            k = re.findall(r'^(?s)while\s*\(.+\)\s*(?!(\s*;))', line)
            k1 = re.findall(r'^(?s)for\s*\(.*;.*;.*\)', line)
            if k or k1:
                code = nest_groups(code, i + 1, 1)
                code = code[:i] + [code[i:i + 2]] + code[i + 2:]
            k2 = re.findall(r'^(?s)do', line)
            if k2:
                code = nest_groups(code, i + 1, 1)
                code = code[:i] + [code[i:i + 3]] + code[i + 3:]
            k3 = re.findall(r'^(?s)if\s*\(.+\)', line)
            if k3:
                code = nest_groups(code, i + 1, 1)
                if i + 2 < len(code) and (type(code[i + 2]) is not list) and re.findall(r'^(?s)\s*else', code[i + 2]):
                    code = nest_groups(code, i + 3, 1)
                    code = code[:i] + [code[i:i + 4]] + code[i + 4:]
                else:
                    code = code[:i] + [code[i:i + 2]] + code[i + 2:]
            if make_list:
                if type(code[i]) is not list:
                    code[i] = [code[i]]
                return code
        i += 1
    return code


def nest(code):
    bracks = []
    i = 0
    while i < len(code):
        if code[i] == '{':
            bracks.append(i)
        elif code[i] == '}':
            match = bracks.pop()
            code = code[:match] + [code[match + 1:i]] + code[i + 1:]
            i = match
        i += 1
    code = nest_groups(code, 0, 0)
    return code
