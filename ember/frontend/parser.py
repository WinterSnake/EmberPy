#!/usr/bin/python
##-------------------------------##
## Ember: Frontend               ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Parser                        ##
##-------------------------------##

## Imports
from pathlib import Path
from typing import Any


## Functions
def parse_lexemes(lexemes: list[tuple[Path, int, int, str]]) -> Any:
    """Return a parse tree from lexemes"""
    lexemes: list[str] = [token[3] for token in lexemes]
    total: int = 0
    nodes: list[Any] = []
    while total < len(lexemes):
        node, i = _parse_expression(lexemes[total:])
        total += i
        nodes.append(node)
    return nodes


def _parse_expression(lexemes: list[str]) -> tuple[Any, int]:
    """Return a parse tree of an expression"""
    if lexemes[0] == "DEBUG__PRINTU__":
        expr, i = _parse_expression_pm(lexemes[2:])  # -Handles 'DEBUG__PRINTU__' and '('
        i += 3  # -Handles 'DEBUG__PRINTU__', '(', and ')'
        expr = {"DEBUG_PRINTU": expr}
    else:
        expr, i = _parse_expression_pm(lexemes)
    return (expr, i + 1)  # -Handles ';'


def _parse_expression_pm(lexemes: list[str]) -> tuple[Any, int]:
    """Return a parse tree of +|- expressions"""
    expr, i = _parse_expression_mdm(lexemes)
    lexemes = lexemes[i:]
    while lexemes and lexemes[0] in ('+', '-'):
        operator: str = lexemes[0]
        rhs, j = _parse_expression_mdm(lexemes[1:])
        expr = {operator:{'lhs': expr, 'rhs': rhs}}
        i += (j := j + 1)
        lexemes = lexemes[j:]
    return (expr, i)


def _parse_expression_mdm(lexemes: list[str]) -> tuple[Any, int]:
    """Return a parse tree of *|/|% expressions"""
    expr, i = _parse_literal_primary(lexemes)
    lexemes = lexemes[i:]
    while lexemes and lexemes[0] in ('*', '/', '%'):
        operator: str = lexemes[0]
        rhs, j = _parse_literal_primary(lexemes[1:])
        expr = {operator:{'lhs': expr, 'rhs': rhs}}
        i += (j := j + 1)
        lexemes = lexemes[j:]
    return (expr, i)


def _parse_literal_primary(lexemes: list[str]) -> tuple[Any, int]:
    """Return a parse tree of a primary literal"""
    if lexemes[0] == '(':
        expr, i = _parse_expression_pm(lexemes[1:])
        return (expr, i + 2)  # -Handles '(' and ')'
    return _parse_literal_number(lexemes)


def _parse_literal_number(lexemes: list[str]) -> tuple[int, int]:
    """Return a parse tree of a number literal"""
    number = int(lexemes[0])
    return (number, 1)
