#!/usr/bin/python
##-------------------------------##
## Ember: Frontend               ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Parser                        ##
##-------------------------------##

## Imports
import sys
from pathlib import Path
from typing import Any

from .lexer import Token


## Functions
def parse_tokens(tokens: list[Token]) -> list[Any] | None:
    """Return a parse tree from lexemes"""
    if not tokens:
        return None
    nodes: list[Any] = []
    index: int = 0
    while index < len(tokens):
        node, j = _parse_expression(tokens[index:])
        nodes.append(node)
        index += j
    return nodes


def _parse_expression(tokens: list[Token]) -> tuple[Any, int]:
    """Return a parse tree of an expression"""
    if tokens[0].type == Token.TYPE.IDENTIFIER and tokens[0].value == "DEBUG__PRINTU__":
        expr, index = _parse_expression_as(tokens[2:])
        index += 3  # -Handles: 'DEBUG__PRINTU__', '(', and ')'
        expr = {"DEBUG_PRINTU": expr}
    else:
        expr, index = _parse_expression_as(tokens)
    # -Handle: Unexpected end of token stream
    if index >= len(tokens):
        token: Token = tokens[-1]
        print(f"{token.file_path.resolve()}:{token.row}:{token.column} Unexpected end of steam, expected ';'")
        sys.exit(1)
    # -Handle: Unexpected token in stream
    elif tokens[index].type != Token.TYPE.SEMICOLON:
        token: Token = tokens[index]
        print(f"{token.file_path.resolve()}:{token.row}:{token.column} Unexpected token '{token}', expected ';'", file=sys.stderr)
        sys.exit(1)
    return (expr, index + 1)  # -Handles ';'


def _parse_expression_as(tokens: list[Token]) -> tuple[Any, int]:
    """Return a parse tree of +|- expressions"""
    expr, index = _parse_expression_mdm(tokens)
    while (
        index < len(tokens) and
        tokens[index].type in (Token.TYPE.ADD, Token.TYPE.SUB)
    ):
        operator: str = tokens[index].type
        rhs, index_ = _parse_expression_mdm(tokens[index + 1:])
        expr = {operator:{'lhs': expr, 'rhs': rhs}}
        index += index_ + 1  # -Handles op and rhs
    return (expr, index)


def _parse_expression_mdm(tokens: list[Token]) -> tuple[Any, int]:
    """Return a parse tree of *|/|% expressions"""
    expr, index = _parse_literal_primary(tokens)
    while (
        index < len(tokens) and
        tokens[index].type in (Token.TYPE.MUL, Token.TYPE.DIV, Token.TYPE.MOD)
    ):
        operator: str = tokens[index].type
        rhs, index_ = _parse_literal_primary(tokens[index + 1:])
        expr = {operator:{'lhs': expr, 'rhs': rhs}}
        index += index_ + 1  # -Handles op and rhs
    return (expr, index)


def _parse_literal_primary(tokens: list[Token]) -> tuple[Any, int]:
    """Return a parse tree of a primary literal"""
    if tokens[0].type == Token.TYPE.LPAREN:
        expr, index = _parse_expression_as(tokens[1:])
        # -Handle: Unexpected token in stream
        if tokens[index + 1].type != Token.TYPE.RPAREN:
            token: Token = tokens[index]
            print(f"{token.file_path.resolve()}:{token.row}:{token.column} Unexpected token '{token}', expected ')'", file=sys.stderr)
            sys.exit(1)
        return (expr, index + 2)  # -Handles '(' and ')'
    return _parse_literal_number(tokens)


def _parse_literal_number(tokens: list[Token]) -> tuple[int, int]:
    """Return a parse tree of a number literal"""
    # -Handle: Unexpected token in stream
    if tokens[0].type != Token.TYPE.NUMBER:
        token: Token = tokens[0]
        print(f"{token.file_path.resolve()}:{token.row}:{token.column} Unexpected token '{token}', expected 'NUMBER'", file=sys.stderr)
        sys.exit(1)
    value: int = int(tokens[0].value)
    return (value, 1)
