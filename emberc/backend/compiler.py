#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Backend: Compile              ##
##-------------------------------##

## Imports
import subprocess
from pathlib import Path
from typing import Any, TextIO, overload

from frontend import Node, ExpressionNode, ValueNode


## Functions
def compile_ast(
    nodes: list[Node], file: Path, assembler_format: str = 's', assemble: bool = True,
    assembly_format: str = 'o', link: bool = True, link_format: str | None = None
) -> Path:
    """Use Compiler Visitor to output AST to an assembly file
    Will return the assembly file if assemble and link are false
    Will return the assembled file if assemble is true and link is false
    Will return the linked file if assemble and link are true"""
    file = file.with_suffix('.' + assembler_format)
    fp: TextIO = file.open('w')
    visitor: Node.Visitor = CompilerVisitor()
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
    for node in nodes:
        text = node.visit(visitor)
        fp.writelines((
            *text,
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
    # -Generate output file/s
    if not assemble:
        return file
    assembled_file: Path = file.with_suffix('.' + assembly_format)
    subprocess.run(["as", str(file), "-o", str(assembled_file)])
    if not link:
        return assembled_file
    linked_file: Path = file.with_suffix('' if link_format is None else ('.' + link_format))
    subprocess.run(["ld", str(assembled_file), "-o", str(linked_file)])
    return linked_file


## Classes
class CompilerVisitor:
    """
    Compiler AST Visitor
    Writes assembly instructions based on node visited
    """

    # -Instance Methods
    def visit_expression_node(self, node: ExpressionNode) -> tuple[str, ...]:
        '''Pops from stack and writes binary expression from lhs and rhs'''
        text: list[str] = []
        text.extend([
            *node.lhs.visit(self),
            *node.rhs.visit(self),
            f"\t# -- {node.operator.name} -- #\n"
            "\tpop %rbx\n",
            "\tpop %rax\n"
        ])
        match node.operator:
            case ExpressionNode.Type.ADD:
                text.extend([
                    "\tadd %rax, %rbx\n",
                    "\tpush %rax\n",
                ])
            case ExpressionNode.Type.SUB:
                text.extend([
                    "\tsub %rax, %rbx\n",
                    "\tpush %rax\n",
                ])
            case ExpressionNode.Type.MUL:
                text.extend([
                    "\timul %rax, %rbx\n",
                    "\tpush %rax\n",
                ])
            case ExpressionNode.Type.DIV:
                text.extend([
                    "\tcqto\n",
                    "\tidiv %rbx\n",
                    "\tpush %rax\n",
                ])
            case ExpressionNode.Type.MOD:
                text.extend([
                    "\tcqto\n",
                    "\tidiv %rbx\n",
                    "\tpush %rdx\n",
                ])
            case _:
                # -TODO: Throw error
                pass
        return tuple(text)

    def visit_value_node(self, node: ValueNode) -> tuple[str, ...]:
        '''Pushes basic node to stack with numeric literal value'''
        return (
            f"\t# -- Push Literal \'{node.value}\' -- #\n",
            f"\tpush {node.value}\n"
        )
