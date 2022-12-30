#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Output                        ##
##-------------------------------##

## Imports
from pathlib import Path
from typing import TextIO


## Functions
def compile_program(program: dict) -> Path:
    """"""
    # -Internal Variables
    file: Path = Path("output.asm")
    fp: TextIO = file.open('w')
    # -Internal Functions
    def pop_expression() -> None:
        ''''''
        fp.writelines((
            "\tpop %rbx\n",
            "\tpop %rax\n"
        ))

    def compile_node(node: dict) -> None:
        ''''''
        if 'value' in node:
            fp.writelines((
                f"\t# -- Push Literal \'{node['value']}\' -- #\n",
                f"\tpush {node['value']}\n"
            ))
        elif 'add' in node:
            compile_node(node['add']['lhs'])
            compile_node(node['add']['rhs'])
            fp.write("\t# -- Add -- #\n")
            pop_expression()
            fp.writelines((
                "\tadd %rax, %rbx\n",
                "\tpush %rax\n",
            ))
        elif 'sub' in node:
            compile_node(node['sub']['lhs'])
            compile_node(node['sub']['rhs'])
            fp.write("\t# -- Sub -- #\n")
            pop_expression()
            fp.writelines((
                "\tsub %rax, %rbx\n",
                "\tpush %rax\n",
            ))
        elif 'mul' in node:
            compile_node(node['mul']['lhs'])
            compile_node(node['mul']['rhs'])
            fp.write("\t# -- Mul -- #\n")
            pop_expression()
            fp.writelines((
                "\timul %rax, %rbx\n",
                "\tpush %rax\n",
            ))
        elif 'div' in node:
            compile_node(node['div']['lhs'])
            compile_node(node['div']['rhs'])
            fp.write("\t# -- Sub -- #\n")
            pop_expression()
            fp.writelines((
                "\tcqto\n",
                "\tidiv %rbx\n",
                "\tpush %rax\n",
            ))
        elif 'mod' in node:
            compile_node(node['mod']['lhs'])
            compile_node(node['mod']['rhs'])
            fp.write("\t# -- Mod -- #\n")
            pop_expression()
            fp.writelines((
                "\tcqto\n",
                "\tidiv %rbx\n",
                "\tpush %rdx\n",
            ))
        else:
            print(f"Unhandled node '{node}' in compile_node")

    # -Body
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
        func: str = node['call']
        compile_node(node['arguments'][0])
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
    return file


def simulate_program(program: dict) -> None:
    """"""
    # -Internal Functions
    def parse_node(node: dict) -> int:
        ''''''
        if 'value' in node:
            return int(node['value'])
        elif 'add' in node:
            lhs: int = parse_node(node['add']['lhs'])
            rhs: int = parse_node(node['add']['rhs'])
            return lhs + rhs
        elif 'sub' in node:
            lhs: int = parse_node(node['sub']['lhs'])
            rhs: int = parse_node(node['sub']['rhs'])
            return lhs - rhs
        elif 'mul' in node:
            lhs: int = parse_node(node['mul']['lhs'])
            rhs: int = parse_node(node['mul']['rhs'])
            return lhs * rhs
        elif 'div' in node:
            lhs: int = parse_node(node['div']['lhs'])
            rhs: int = parse_node(node['div']['rhs'])
            return lhs // rhs
        elif 'mod' in node:
            lhs: int = parse_node(node['mod']['lhs'])
            rhs: int = parse_node(node['mod']['rhs'])
            return lhs % rhs
        else:
            print(f"Unhandled node: {node}")

    # -Body
    for node in program:
        func: str = node['call']
        arg0: int = parse_node(node['arguments'][0])
        # -Simulate Function Call
        print(arg0)
