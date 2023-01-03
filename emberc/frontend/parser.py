#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Parser                        ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Iterator
from typing import Any, cast

from .lexer import Lexer
from .token import Token


## Constants
EXPRESSIONS = {
    Token.Type.ADD: "add",
    Token.Type.SUB: "sub",
    Token.Type.MUL: "mul",
    Token.Type.DIV: "div",
    Token.Type.MOD: "mod",
}


## Classes
class Parser:
    """"""

    # -Constructor
    def __init__(self, token_generator: Iterator[Token]) -> None:
        self._token_generator: Iterator[Token] = token_generator
        self._token_buffer: Token | None = None

    # -Instance Methods: Private
    def _advance(self, _type: Token.Type) -> Token | None:
        ''''''
        token: Token | None = self._next()
        # -TODO: Error handling on invalid token type
        if token is None:
            print(f"Unexpected end of stream, expected '{_type}'")
        elif token.type != _type:
            print(f"Unexpected token '{token.type}', expected '{_type}'")
        return token

    def _check(self, _type: Token.Type) -> bool:
        ''''''
        token: Token | None = self._next()
        if token is None or token.type != _type:
            self._token_buffer = token
            return False
        return True

    def _next(self) -> Token | None:
        ''''''
        if self._token_buffer:
            token: Token | None = self._token_buffer
            self._token_buffer = None
            return token
        return next(self._token_generator, None)

    def _peek(self) -> Token | None:
        ''''''
        token: Token | None = self._next()
        self._token_buffer = token
        return token

    # -Instance Methods: Parsing
    def _parse_statement(self) -> dict[str, Any]:
        ''''''
        statement: dict[str, Any] = self._parse_expression()
        self._advance(Token.Type.SEMICOLON)
        return statement

    def _parse_expression(self) -> dict[str, Any]:
        ''''''
        return self._parse_expression_term()

    def _parse_expression_term(self) -> dict[str, Any]:
        ''''''
        expr = self._parse_expression_factor()
        while cast(Token, self._peek()).type in (
            Token.Type.ADD, Token.Type.SUB
        ):
            token: Token = cast(Token, self._next())
            rhs = self._parse_expression_factor()
            expr = {EXPRESSIONS[token.type]: {'lhs': expr, 'rhs': rhs}}
        return expr

    def _parse_expression_factor(self) -> dict[str, Any]:
        ''''''
        expr = self._parse_expression_primary()
        while cast(Token, self._peek()).type in (
            Token.Type.MUL, Token.Type.DIV, Token.Type.MOD
        ):
            token: Token = cast(Token, self._next())
            rhs = self._parse_literal_numeric()
            expr = {EXPRESSIONS[token.type]: {'lhs': expr, 'rhs': rhs}}
        return expr

    def _parse_expression_primary(self) -> dict[str, Any]:
        ''''''
        if self._check(Token.Type.LPAREN):
            expr: dict[str, Any] = self._parse_expression()
            self._advance(Token.Type.RPAREN)
            return expr
        return self._parse_literal_numeric()

    def _parse_literal_numeric(self) -> dict[str, Any]:
        ''''''
        negate: bool = self._check(Token.Type.SUB)
        token: Token = cast(Token, self._advance(Token.Type.NUMERIC))
        return {'value': ('-' if negate else '') + cast(str, token.value)}

    # -Instance Methods: Public
    def parse(self) -> list[dict[str, Any]]:
        ''''''
        nodes: list[dict[str, Any]] = []
        while self._peek():
            node: dict[str, Any] = self._parse_statement()
            nodes.append(node)
        return nodes

    # -Class Methods
    @classmethod
    def from_lexer(cls, lexer: Lexer) -> Parser:
        return cls(lexer.next_token())

    @classmethod
    def from_list(cls, tokens: list[Token]) -> Parser:
        return cls(iter(tokens))
