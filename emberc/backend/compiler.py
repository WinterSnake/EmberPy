#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Backend: Compile              ##
##-------------------------------##

## Imports
from pathlib import Path
from typing import Any, TextIO

from frontend import Node, ExpressionNode, ValueNode


## Functions
def compile_program(program: list[Node], file: Path) -> None:
    """"""
    fp: TextIO = file.open('w')
    compiler: CompilerVisitor = CompilerVisitor()
    fp.writelines((
        ".intel_syntax\n",
        ".text\n",
        ".global _start\n",
        ".global __PRINTU__\n",
        "__PRINTU__:\n",
        "\tsub	%rsp, 40\n",
        "\tmov	%ecx, 1\n",
        "\tmov	%r9d, 31\n",
        "\tmov	%r8d, 10\n",
        "\tmov	BYTE PTR 31[%rsp], 10\n",
        ".L2:\n",
        "\tmovzx	%eax, %cx\n",
        "\tmov	%esi, %r9d\n",
        "\txor	%edx, %edx\n",
        "\tinc	%ecx\n",
        "\tsub	%esi, %eax\n",
        "\tmov	%rax, %rdi\n",
        "\tdiv	%r8\n",
        "\tmovsx	%rsi, %esi\n",
        "\tadd	%edx, 48\n",
        "\tmov	BYTE PTR [%rsp+%rsi], %dl\n",
        "\tmov	%rdx, %rdi\n",
        "\tmov	%rdi, %rax\n",
        "\tcmp	%rdx, 9\n",
        "\tja	.L2\n",
        "\tmovzx	%edx, %cx\n",
        "\tmov	%eax, 32\n",
        "\tmovzx	%ecx, %cx\n",
        "\tmov	%edi, 1\n",
        "\tsub	%eax, %ecx\n",
        "\tcdqe\n",
        "\tlea	%rsi, [%rsp+%rax]\n",
        "\tmov %rax, 1\n",
        "\tsyscall\n",
        "\tadd %rsp, 40\n",
        "\tret\n\n",
        "_start:\n"
    ))
    for node in program:
        node.visit(compiler, fp)
        fp.writelines((
            "\t# -- DEBUG__PRINTU__ -- #\n",
            "\tpop %rdi\n",
            "\tcall __PRINTU__\n"
        ))
    # - Write Sysexit
    fp.writelines((
        "\t# -- exit -- #\n",
        "\tmov %rax, 60\n",
        "\txor %rdi, %rdi\n",
        "\tsyscall\n"
    ))
    fp.close()


## Classes
class CompilerVisitor(Node.Visitor):
    """"""

    # -Instance Methods
    def visit_expression_node(self, node: ExpressionNode, fp: TextIO) -> None:
        node.lhs.visit(self, fp)
        node.rhs.visit(self, fp)
        fp.writelines((
            "\tpop %rbx\n",
            "\tpop %rax\n"
        ))
        match node.operator:
            case ExpressionNode.Type.ADD:
                fp.write("\t# -- Add -- #\n")
                fp.writelines((
                    "\tadd %rax, %rbx\n",
                    "\tpush %rax\n",
                ))
            case ExpressionNode.Type.SUB:
                fp.write("\t# -- Sub -- #\n")
                fp.writelines((
                    "\tsub %rax, %rbx\n",
                    "\tpush %rax\n",
                ))
            case ExpressionNode.Type.MUL:
                fp.write("\t# -- Mul -- #\n")
                fp.writelines((
                    "\timul %rax, %rbx\n",
                    "\tpush %rax\n",
                ))
            case ExpressionNode.Type.DIV:
                fp.write("\t# -- Div -- #\n")
                fp.writelines((
                    "\tcqto\n",
                    "\tidiv %rbx\n",
                    "\tpush %rax\n",
                ))
            case ExpressionNode.Type.MOD:
                fp.write("\t# -- Mod -- #\n")
                fp.writelines((
                    "\tcqto\n",
                    "\tidiv %rbx\n",
                    "\tpush %rdx\n",
                ))
            case _:
                # -TODO: Throw error
                pass

    def visit_value_node(self, node: ValueNode, fp: TextIO) -> None:
        fp.writelines((
            f"\t# -- Push Literal \'{node.value}\' -- #\n",
            f"\tpush {node.value}\n"
        ))
