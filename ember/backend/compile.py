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
    f.write(".globl __start__\n")
    _compile_debug(f)
    f.write("__start__:\n")
    for node in nodes:
        _compile_node(node, f)
    f.write("# -- exit -- #\n")
    f.write("\tmovq $60, %rax\n")
    f.write("\txor %rdi, %rdi\n")
    f.write("\tsyscall\n")
    f.close()
    return file


def _compile_debug(file: TextIO) -> None:
    """Compile debug functions"""
    file.write(".globl  DEBUG__PRINTI__\n")
    file.write("DEBUG__PRINTU__:\n")
    file.write("\tmovabsq $-3689348814741910323, %r9\n")
    file.write("\tsubq $40, %rsp\n")
    file.write("\tmovb $10, 31(%rsp)\n")
    file.write("\tleaq 30(%rsp), %rcx\n")
    file.write(".L2:\n")
    file.write("\tmovq %rdi, %rax\n")
    file.write("\tleaq 32(%rsp), %r8\n")
    file.write("\tmulq %r9\n")
    file.write("\tmovq %rdi, %rax\n")
    file.write("\tsubq %rcx, %r8\n")
    file.write("\tshrq $3, %rdx\n")
    file.write("\tleaq (%rdx,%rdx,4), %rsi\n")
    file.write("\taddq %rsi, %rsi\n")
    file.write("\tsubq %rsi, %rax\n")
    file.write("\taddl $48, %eax\n")
    file.write("\tmovb %al, (%rcx)\n")
    file.write("\tmovq %rdi, %rax\n")
    file.write("\tmovq %rdx, %rdi\n")
    file.write("\tmovq %rcx, %rdx\n")
    file.write("\tsubq $1, %rcx\n")
    file.write("\tcmpq $9, %rax\n")
    file.write("\tja .L2\n")
    file.write("\tleaq 32(%rsp), %rax\n")
    file.write("\tmovl $1, %edi\n")
    file.write("\tsubq %rax, %rdx\n")
    file.write("\tleaq 32(%rsp,%rdx), %rsi\n")
    file.write("\tmovq %r8, %rdx\n")
    file.write("\tmovq $1, %rax\n")
    file.write("\tsyscall\n")
    file.write("\taddq $40, %rsp\n")
    file.write("\tret\n")


def _compile_node(node: Any, file: TextIO) -> None:
    """Compile a single node"""
    if isinstance(node, int):
        file.write(f"# -- push {node} -- #\n")
        file.write(f"\tpush ${node}\n")
    elif isinstance(node, dict):
        op: str = list(node.keys())[0]
        if op in ('+', '-', '*', '/', '%'):
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
        elif op == "DEBUG_PRINTU":
            _compile_node(node[op], file)
            file.write("# -- debug print -- #\n")
            file.write("\tpop %rdi\n")
            file.write("\tcall DEBUG__PRINTU__\n")
