import re
import sys
import os
import ast

args = sys.argv
directory = args[1]


def argument_recognition():
    files_list = []
    if directory.endswith('.py'):
        files_list.append(directory)
    else:
        temp_list = os.listdir(directory)
        for dic in temp_list:
            files_list.append(f'{directory}\{dic}')
    return files_list


def soo1_error(line, count, file):
    if len(str(line)) > 79:
        print(f'{file}: Line {count}: S001 Too long')


def soo2_error(line, count, file):
    empty_spaces = 0
    for ch in line:
        if ch == ' ':
            empty_spaces += 1
        else:
            if (empty_spaces % 4) != 0:
                print(f'{file}: Line {count}: S002 Indentation is not a multiple of four')
                break
            else:
                break


def soo3_error(line, count, file):
    index = 0
    for ch in line:
        if ch == ";":
            if line[index - 1] == ')' or line[index - 1] == ';':
                print(f'{file}: Line {count}: S003 Unnecessary semicolon')
                break
        index += 1


def soo4_error(line, count, file):
    index = 0
    hash_count = 0
    for ch in line:
        if ch == "#":
            if hash_count == 1:
                break
            elif index == 0:
                break
            elif line[index - 1] != ' ' or line[index - 2] != ' ':
                print(f'{file}: Line {count}: S004 At least two spaces required before inline comments')
                break
            hash_count += 1
        index += 1


def soo5_error(line, count, file):
    if re.match('.*?# [Tt][Oo][Dd][Oo]', line):
        print(f'{file}: Line {count}: S005 TODO found')


def soo78_error(line, count, file):
    if line.startswith('class'):
        if line[5] == ' ' and line[6] == ' ':
            print(f"{file}: Line {count}: S007 Too many spaces after 'class'")
        elif line[6].isupper() is False:
            print(f"{file}: Line {count}: S008 Class name 'user' should use CamelCase")


def soo9_error(line, count, file):
    if re.match(r'.*?def\s\s+.*?', line):
        print(f"{file}: Line {count}: S007 Too many spaces after 'def'")
    elif matches := re.match(r"^[ ]*def (?P<name>\w+)", line):
        if not re.match(r"[a-z_]+", matches["name"]):
            print(f"{file}: Line {count}: S009 Function name should use snake_case")


def sooast_error(count, file):
    script = open(file).read()
    tree = ast.parse(script)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                function = arg.arg
                if not re.match(r"[a-z_]+", function):
                    if arg.lineno == count:
                        print(f"{file}: Line {arg.lineno}: S010 Argument name {function} should be written in snake_case")
            for item in node.args.defaults:
                if isinstance(item, ast.List):
                    if item.lineno == count:
                        print(f"{file}: Line {item.lineno}: S012 Default argument value is mutable")
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                function = node.id
                if not re.match(r"[a-z_]+", function):
                    if node.lineno == count:
                        print(f"{file}: Line {node.lineno}: S011 Variable {function} should be written in snake_case")


def input_file():
    file_names = argument_recognition()
    for file in file_names:
        if file.endswith('.py') is True:
            with open(file, 'r') as f:
                lines = f.readlines()
                count = 1
                empty_lines = 0
                for line in lines:
                    soo1_error(line, count, file)
                    soo2_error(line, count, file)
                    soo3_error(line, count, file)
                    soo4_error(line, count, file)
                    soo5_error(line, count, file)
                    soo78_error(line, count, file)
                    soo9_error(line, count, file)
                    sooast_error(count, file)
                    if line == "\n":
                        empty_lines += 1
                    elif len(line) != 0:
                        if empty_lines >= 3:
                            print(f'{file}: Line {count}: S006 More than two blank lines used before this line')
                            empty_lines = 0
                        else:
                            empty_lines = 0
                    count += 1


input_file()
