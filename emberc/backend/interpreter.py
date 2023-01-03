#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Backend: Interpreter          ##
##-------------------------------##

## Imports
from typing import Any


## Functions
def interpret_program(program: list[dict[str, Any]]) -> None:
    """"""
    # -Internal Functions
    def parse_node(node: dict[str, Any]) -> int:
        ''''''
        if 'value' in node:
            return int(node['value'])
        elif 'add' in node:
            lhs: int = parse_node(node['add']['lhs'])
            rhs: int = parse_node(node['add']['rhs'])
            return lhs + rhs
        elif 'sub' in node:
            lhs = parse_node(node['sub']['lhs'])
            rhs = parse_node(node['sub']['rhs'])
            return lhs - rhs
        elif 'mul' in node:
            lhs = parse_node(node['mul']['lhs'])
            rhs = parse_node(node['mul']['rhs'])
            return lhs * rhs
        elif 'div' in node:
            lhs = parse_node(node['div']['lhs'])
            rhs = parse_node(node['div']['rhs'])
            return lhs // rhs
        elif 'mod' in node:
            lhs = parse_node(node['mod']['lhs'])
            rhs = parse_node(node['mod']['rhs'])
            return lhs % rhs
        else:
            print(f"Unhandled node: {node}")
            return None  # type: ignore

    # -Body
    for node in program:
        print(parse_node(node))
