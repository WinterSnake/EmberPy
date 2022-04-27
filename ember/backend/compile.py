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

from frontend.token import Token


## Functions
def compile_ast(nodes: list[Any], file: Path) -> None:
    """Compile an ast"""
    with file.open('w') as f:
        f.writelines([
            ".text\n",
            ".globl __start__\n",
            ".globl  DEBUG__PRINTU__\n",
            "DEBUG__PRINTU__:\n",
            "\tmovabsq $-3689348814741910323, %r9\n",
            "\tsubq $40, %rsp\n",
            "\tmovb $10, 31(%rsp)\n",
            "\tleaq 30(%rsp), %rcx\n",
            ".L2:\n",
            "\tmovq %rdi, %rax\n",
            "\tleaq 32(%rsp), %r8\n",
            "\tmulq %r9\n",
            "\tmovq %rdi, %rax\n",
            "\tsubq %rcx, %r8\n",
            "\tshrq $3, %rdx\n",
            "\tleaq (%rdx,%rdx,4), %rsi\n",
            "\taddq %rsi, %rsi\n",
            "\tsubq %rsi, %rax\n",
            "\taddl $48, %eax\n",
            "\tmovb %al, (%rcx)\n",
            "\tmovq %rdi, %rax\n",
            "\tmovq %rdx, %rdi\n",
            "\tmovq %rcx, %rdx\n",
            "\tsubq $1, %rcx\n",
            "\tcmpq $9, %rax\n",
            "\tja .L2\n",
            "\tleaq 32(%rsp), %rax\n",
            "\tmovl $1, %edi\n",
            "\tsubq %rax, %rdx\n",
            "\tleaq 32(%rsp,%rdx), %rsi\n",
            "\tmovq %r8, %rdx\n",
            "\tmovq $1, %rax\n",
            "\tsyscall\n",
            "\taddq $40, %rsp\n",
            "\tret\n",
            "__start__:\n"
        ])
        for node in nodes:
            node.compile(f)
        f.writelines([
            "# -- exit -- #\n",
            "\tmovq $60, %rax\n",
            "\txor %rdi, %rdi\n",
            "\tsyscall\n",
        ])
