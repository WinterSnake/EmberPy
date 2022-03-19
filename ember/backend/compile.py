#!/usr/bin/python
##-------------------------------##
## Ember: Backend                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Compile                       ##
##-------------------------------##

## Imports
from pathlib import Path
from typing import Any, TextIO


## Functions
def compile_ast(nodes: list[Any], file_name: str) -> Path:
    """Compile an ast"""
    file: Path = Path(file_name)
    f: TextIO = file.open('w')
    f.write(".text\n")
    f.write(".global __start__\n")
    f.write("__start__:\n")
    for node in nodes:
        _compile_node(node, f)
    f.write("\tmov $60, %rax\n")
    f.write("\tpop %rdi\n")
    f.write("\tsyscall\n")
    f.close()
    return file


def _compile_node(node: Any, file: TextIO) -> None:
    """Compile a single node"""
    if isinstance(node, int):
        file.write(f"# -- push {node} -- #\n")
        file.write(f"\tpush ${node}\n")
    elif isinstance(node, dict):
        op: str = list(node.keys())[0]
        _compile_node(node[op]['lhs'], file)
        _compile_node(node[op]['rhs'], file)
        if op == '+':
            file.write("# -- add -- #\n")
            file.write("\tpop %rbx\n")
            file.write("\tpop %rax\n")
            file.write("\taddq %rbx, %rax\n")
            file.write("\tpush %rax\n")
        elif op == '-':
            file.write("# -- sub -- #\n")
            file.write("\tpop %rbx\n")
            file.write("\tpop %rax\n")
            file.write("\tsubq %rbx, %rax\n")
            file.write("\tpush %rax\n")
        elif op == '*':
            file.write("# -- mul -- #\n")
            file.write("\tpop %rbx\n")
            file.write("\tpop %rax\n")
            file.write("\timulq %rbx, %rax\n")
            file.write("\tpush %rax\n")
        elif op == '/':
            file.write("# -- div -- #\n")
            file.write("\tpop %rbx\n")
            file.write("\tpop %rax\n")
            file.write("\tcqto\n")
            file.write("\tidivq %rbx\n")
            file.write("\tpush %rax\n")
        elif op == '%':
            file.write("# -- mod -- #\n")
            file.write("\tpop %rbx\n")
            file.write("\tpop %rax\n")
            file.write("\tcqto\n")
            file.write("\tidivq %rbx\n")
            file.write("\tpush %rdx\n")
