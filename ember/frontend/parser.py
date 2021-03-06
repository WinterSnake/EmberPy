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
from typing import Any, cast

from .token import Token
from .node import NodeBase, NodeStatement, NodeExpression, NodeLiteral

## Constants
LOOKUP: dict[Token.TYPE, NodeExpression.OPERATOR] = {
    Token.TYPE.ADD: NodeExpression.OPERATOR.ADD,
    Token.TYPE.SUB: NodeExpression.OPERATOR.SUB,
    Token.TYPE.MUL: NodeExpression.OPERATOR.MUL,
    Token.TYPE.DIV: NodeExpression.OPERATOR.DIV,
    Token.TYPE.MOD: NodeExpression.OPERATOR.MOD,
    Token.TYPE.EQUEQU: NodeExpression.OPERATOR.EQUEQU,
    Token.TYPE.NOTEQU: NodeExpression.OPERATOR.NOTEQU,
}


## Functions
def parse_program(tokens: list[Token]) -> list[NodeBase] | None:
    """Return a parse tree from list of tokens"""
    _parser_check()
    if not tokens:
        return None
    nodes: list[Any] = []
    index: int = 0
    while index < len(tokens):
        node, j = _parse_statement(tokens[index:])
        nodes.append(node)
        index += j
    return nodes


def _parser_check() -> None:
    """Checks if all current token types are handled by the parser"""
    unhandled_token_types: tuple[Token.TYPE, ...] = tuple(
        type_
        for type_ in Token.TYPE
        if type_ not in (
            # -KEYWORD
            # -LITERAL
            Token.TYPE.IDENTIFIER,
            Token.TYPE.NUMBER,
            # -COMPARISON
            Token.TYPE.EQUEQU,
            Token.TYPE.NOTEQU,
            # -SYMBOL
            Token.TYPE.ADD,
            Token.TYPE.SUB,
            Token.TYPE.MUL,
            Token.TYPE.DIV,
            Token.TYPE.MOD,
            Token.TYPE.SEMICOLON,
            Token.TYPE.LPAREN,
            Token.TYPE.RPAREN,
        )
    )
    if not unhandled_token_types:
        return None
    raise NotImplementedError(
        "Parser unable to handle the following tokens: {}".format(
            ", ".join(f"'{type_.name}'" for type_ in unhandled_token_types)
        )
    )


def _parse_statement(tokens: list[Token]) -> tuple[NodeBase, int]:
    """Return a parse tree of an expression"""
    token: Token
    nindex: int = 0;
    if tokens[0].type == Token.TYPE.IDENTIFIER and tokens[0].value == "DEBUG__PRINTU__":
        tokens = tokens[2:]  # -Handles: 'DEBUG__PRINTU__', and '('
        nindex = 3
    expr, index = _parse_expression(tokens)
    if nindex:
        index += 1  # -Handles ')'
        expr = NodeStatement(cast(NodeExpression, expr))
    # -Handle: Unexpected end of token stream
    if index >= len(tokens):
        token = tokens[-1]
    # -Handle: Unexpected token in stream
    elif tokens[index].type != Token.TYPE.SEMICOLON:
        token = tokens[index]
        print(f"{token.file_path.resolve()}:{token.row}:{token.column} Unexpected token '{token}', expected ';'", file=sys.stderr)
        sys.exit(1)
    return (expr, index + nindex + 1)  # -Handles ';'


def _parse_expression(tokens: list[Token]) -> tuple[NodeBase, int]:
    """Return an expression parse tree"""
    return _parse_expression_equality(tokens)


def _parse_expression_equality(tokens: list[Token]) -> tuple[NodeBase, int]:
    """Return a parse tree of ==|!= comparisons"""
    expr, index = _parse_expression_as(tokens)
    while (
        index < len(tokens) and
        tokens[index].type in (Token.TYPE.EQUEQU, Token.TYPE.NOTEQU)
    ):
        operator: NodeExpression.OPERATOR = LOOKUP[tokens[index].type]
        rhs, j = _parse_expression_as(tokens[index + 1:])
        expr = NodeExpression(operator, lhs=expr, rhs=rhs)
        index += j + 1  # -Handles op and rhs
    return (expr, index)


def _parse_expression_as(tokens: list[Token]) -> tuple[NodeBase, int]:
    """Return a parse tree of +|- expressions"""
    expr, index = _parse_expression_mdm(tokens)
    while (
        index < len(tokens) and
        tokens[index].type in (Token.TYPE.ADD, Token.TYPE.SUB)
    ):
        operator: NodeExpression.OPERATOR = LOOKUP[tokens[index].type]
        rhs, j = _parse_expression_mdm(tokens[index + 1:])
        expr = NodeExpression(operator, lhs=expr, rhs=rhs)
        index += j + 1  # -Handles op and rhs
    return (expr, index)


def _parse_expression_mdm(tokens: list[Token]) -> tuple[NodeBase, int]:
    """Return a parse tree of *|/|% expressions"""
    expr, index = _parse_literal_primary(tokens)
    while (
        index < len(tokens) and
        tokens[index].type in (Token.TYPE.MUL, Token.TYPE.DIV, Token.TYPE.MOD)
    ):
        operator: NodeExpression.OPERATOR = LOOKUP[tokens[index].type]
        rhs, j = _parse_literal_primary(tokens[index + 1:])
        expr = NodeExpression(operator, lhs=expr, rhs=rhs)
        index += j + 1  # -Handles op and rhs
    return (expr, index)


def _parse_literal_primary(tokens: list[Token]) -> tuple[NodeBase, int]:
    """Return a parse tree of a primary literal"""
    if tokens[0].type == Token.TYPE.LPAREN:
        expr, index = _parse_expression(tokens[1:])
        # -Handle: Unexpected token in stream
        if tokens[index + 1].type != Token.TYPE.RPAREN:
            token: Token = tokens[index + 1]
            print(f"{token.file_path.resolve()}:{token.row}:{token.column} Unexpected token '{token}', expected ')'", file=sys.stderr)
            sys.exit(1)
        return (expr, index + 2)  # -Handles '(' and ')'
    return _parse_literal_number(tokens)


def _parse_literal_number(tokens: list[Token]) -> tuple[NodeLiteral, int]:
    """Return a parse tree of a number literal"""
    index: int = 0
    # -Handle negatives
    negate: bool = False
    if tokens[0].type == Token.TYPE.SUB:
        index += 1
        negate = True
    # -Handle: Unexpected token in stream
    if tokens[0].type != Token.TYPE.NUMBER:
        token: Token = tokens[0]
        print(f"{token.file_path.resolve()}:{token.row}:{token.column} Unexpected token '{token}', expected 'NUMBER'", file=sys.stderr)
        sys.exit(1)
    value: int = int(cast(str, tokens[index].value))
    if negate:
        value *= -1
    return (NodeLiteral(value=value), index + 1)  # -Handles NUMBER literal
