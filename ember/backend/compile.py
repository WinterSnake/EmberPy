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
    f.writelines([
        "# -- exit -- #\n",
        "\tmovq $60, %rax\n",
        "\txor %rdi, %rdi\n",
        "\tsyscall\n",
    ])
    f.close()
    return file


def _compile_debug(file: TextIO) -> None:
    """Compile debug functions"""
    file.writelines([
        ".globl  DEBUG__PRINTI__\n",
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
    ])


def _compile_node(node: Any, file: TextIO) -> None:
    """Compile a single node"""
    if isinstance(node, int):
        file.writelines([
            f"# -- push {node} -- #\n",
            f"\tpush ${node}\n",
        ])
    elif isinstance(node, dict):
        op: str = list(node.keys())[0]
        if op in (
            Token.TYPE.ADD, Token.TYPE.SUB, Token.TYPE.MUL,
            Token.TYPE.DIV, Token.TYPE.MOD
        ):
            _compile_node(node[op]['lhs'], file)
            _compile_node(node[op]['rhs'], file)
            if op == Token.TYPE.ADD:
                file.writelines([
                    "# -- add -- #\n",
                    "\tpop %rbx\n",
                    "\tpop %rax\n",
                    "\taddq %rbx, %rax\n",
                    "\tpush %rax\n",
                ])
            elif op == Token.TYPE.SUB:
                file.writelines([
                    "# -- sub -- #\n",
                    "\tpop %rbx\n",
                    "\tpop %rax\n",
                    "\tsubq %rbx, %rax\n",
                    "\tpush %rax\n",
                ])
            elif op == Token.TYPE.MUL:
                file.writelines([
                    "# -- mul -- #\n",
                    "\tpop %rbx\n",
                    "\tpop %rax\n",
                    "\timulq %rbx, %rax\n",
                    "\tpush %rax\n",
                ])
            elif op == Token.TYPE.DIV:
                file.writelines([
                    "# -- div -- #\n",
                    "\tpop %rbx\n",
                    "\tpop %rax\n",
                    "\tcqto\n",
                    "\tidivq %rbx\n",
                    "\tpush %rax\n",
                ])
            elif op == Token.TYPE.MOD:
                file.writelines([
                    "# -- mod -- #\n",
                    "\tpop %rbx\n",
                    "\tpop %rax\n",
                    "\tcqto\n",
                    "\tidivq %rbx\n",
                    "\tpush %rdx\n",
                ])
            elif op == Token.TYPE.EQUEQU:
                file.writelines([
                    "# -- comparison: equal -- #\n",
                    "\tpop %rbx\n",
                    "\tpop %rax\n",
                    "\tcmpq %rbx, %rax\n",
                    "\tsete %al\n",
                    "\t"
                ])
        elif op == "DEBUG_PRINTU":
            _compile_node(node[op], file)
            file.writelines([
                "# -- debug print -- #\n",
                "\tpop %rdi\n",
                "\tcall DEBUG__PRINTU__\n",
            ])
