#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Parser              ##
##-------------------------------##

## Imports
from __future__ import annotations

from .lexer import Lexer, TokenGenerator
from .node import (
    Node, NodeBinaryExpression, NodeLiteral,
)
from .token import Token

## Constants
__all__: tuple[str] = ("Parser",)
OPERATORS: dict[Token.Type, NodeBinaryExpression.Type] = {
    Token.Type.Plus: NodeBinaryExpression.Type.Add,
    Token.Type.Minus: NodeBinaryExpression.Type.Sub,
    Token.Type.Asterisk: NodeBinaryExpression.Type.Mul,
    Token.Type.FSlash: NodeBinaryExpression.Type.Div,
    Token.Type.Percent: NodeBinaryExpression.Type.Mod,
}


## Classes
class Parser:
    """
    Ember Language Recursive Descent Parser
    Lookahead(1) Operation
    """

    # -Constructor
    def __init__(self, token_generator: TokenGenerator) -> None:
        self._current_token: Token | None = None
        self.tokens: TokenGenerator = token_generator

    # -Dunder Methods
    def __repr__(self) -> str:
        return ""

    def __str__(self) -> str:
        return ""

    # -Instance Methods
    def _next(self) -> Token | None:
        ''''''
        if self._current_token is not None:
            token = self._current_token
            self._current_token = None
            return token
        return next(self.tokens, None)

    def _peek(self) -> Token | None:
        ''''''
        token = self._next()
        self._current_token = token
        return token

    def _match(self, *types: Token.Type) -> bool:
        ''''''
        token = self._peek()
        if token is not None and token.type in types:
            return True
        return False

    def _consume(self, _type: Token.Type) -> bool:
        ''''''
        token = self._peek()
        if token is not None and token.type == _type:
            self._next()
            return True
        return False

    def parse(self) -> Node:
        ''''''
        nodes = []
        while self._peek():
            node = self._parse_binary_expression()
            # -TODO: Syntax Error
            token = self._next()
            nodes.append(node)
        return nodes

    def _parse_binary_expression(self) -> Node:
        ''''''
        node = self._parse_term_expression()
        return node

    def _parse_term_expression(self) -> Node:
        ''''''
        node = self._parse_factor_expression()
        while self._match(Token.Type.Plus, Token.Type.Minus):
            op = self._next()
            rhs = self._parse_factor_expression()
            _type = OPERATORS.get(op.type)
            assert _type is not None
            node = NodeBinaryExpression(node, rhs, _type)
        return node

    def _parse_factor_expression(self) -> Node:
        ''''''
        node = self._parse_primary_expression()
        while self._match(Token.Type.Asterisk, Token.Type.FSlash, Token.Type.Percent):
            op = self._next()
            rhs = self._parse_primary_expression()
            _type = OPERATORS.get(op.type)
            assert _type is not None
            node = NodeBinaryExpression(node, rhs, _type)
        return node

    def _parse_primary_expression(self) -> Node:
        ''''''
        if self._consume(Token.Type.LParen):
            node = self._parse_binary_expression()
            # -TODO: Syntax Error
            self._consume(Token.Type.RParen)
            return node
        node = self._parse_literal()
        return node

    def _parse_literal(self) -> NodeLiteral:
        ''''''
        token = self._next()
        # -TODO: Syntax Error
        if token.type != Token.Type.Number:
            print(f"Expected Number token, found: {token.type.name}")
        assert token.value is not None
        return NodeLiteral(int(token.value))

    # -Class Methods
    @classmethod
    def from_lexer(cls, lexer: Lexer) -> Parser:
        ''''''
        return cls(lexer.lex())
