#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Parser                        ##
##-------------------------------##

## Imports
from typing import Any

from token import Token


## Constants
EXPRESSIONS = {
    Token.Type.ADD: "add",
    Token.Type.SUB: "sub",
    Token.Type.MUL: "mul",
    Token.Type.DIV: "div",
    Token.Type.MOD: "mod",
}


## Functions
def consume_token(
    tokens: list[Token], _type: Token.Type, value: str | None = None
) -> Token | None:
    """"""
    token: Token = tokens.pop(0)
    if not token.type == _type:
        print(f"Invalid token. Expected: '{_type.name}', got: '{token.type.name}'")
        token = None  # type: ignore
    elif value is not None and token.value != value:
        print(f"Invalid value. Expected: '{value}', got: '{token.value}'")
        token = None  # type: ignore
    return token


def check_next_token(tokens: list[Token], types: tuple[Token.Type, ...]) -> bool:
    """"""
    return tokens[0].type in types


def parse_program(tokens: list[Token]) -> list[dict[str, Any]] | None:
    """"""
    if not tokens:
        return None
    nodes = []
    while tokens:
        node = parse_expression(tokens)
        nodes.append(node)
    return nodes


def parse_expression(tokens: list[Token]) -> dict[str, Any]:
    """"""
    consume_token(tokens, Token.Type.IDENTIFIER, value="DEBUG__PRINTU__")
    consume_token(tokens, Token.Type.LPAREN)
    node = parse_expression_add_or_sub(tokens)
    consume_token(tokens, Token.Type.RPAREN)
    consume_token(tokens, Token.Type.SEMICOLON)
    node = {'call': "DEBUG__PRINTU__", 'arguments': [node]}
    return node


def parse_expression_add_or_sub(tokens: list[Token]) -> dict[str, Any]:
    """"""
    node = parse_expression_mul_or_div_or_mod(tokens)
    while check_next_token(tokens, (Token.Type.ADD, Token.Type.SUB)):
        expr = EXPRESSIONS[tokens.pop(0).type]
        rhs = parse_expression_mul_or_div_or_mod(tokens)
        node = {expr: {'lhs': node, 'rhs': rhs}}
    return node


def parse_expression_mul_or_div_or_mod(tokens: list[Token]) -> dict[str, Any]:
    """"""
    node = parse_digit(tokens)
    while check_next_token(tokens, (Token.Type.MUL, Token.Type.DIV, Token.Type.MOD)):
        expr = EXPRESSIONS[tokens.pop(0).type]
        rhs = parse_digit(tokens)
        node = {expr: {'lhs': node, 'rhs': rhs}}  # type: ignore
    return node


def parse_digit(tokens: list[Token]) -> dict[str, str]:
    """"""
    negate = check_next_token(tokens, (Token.Type.SUB, ))
    if negate:
        tokens.pop(0)
    token = consume_token(tokens, Token.Type.NUMERIC)
    return {"value": ('-' if negate else '') + token.value}  # type: ignore
