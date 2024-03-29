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
from .node import Node, CallNode, ExpressionNode, ValueNode
from .token import Token


## Constants
EXPRESSIONS = {
    Token.Type.ADD: ExpressionNode.Type.ADD,
    Token.Type.SUB: ExpressionNode.Type.SUB,
    Token.Type.MUL: ExpressionNode.Type.MUL,
    Token.Type.DIV: ExpressionNode.Type.DIV,
    Token.Type.MOD: ExpressionNode.Type.MOD,
}


## Classes
class Parser:
    """
    Ember Recursive Descent Parser
    Each internal parsing method represents a rule from the EBNF
    Lookahead(1) operation
    """

    # -Constructor
    def __init__(self, token_generator: Iterator[Token]) -> None:
        self._token_generator: Iterator[Token] = token_generator
        self._token_buffer: Token | None = None

    # -Instance Methods: Private
    def _advance(self, _type: Token.Type) -> Token | None:
        '''Advanced to next token and assert its of expected type.
        End parsing on failure or end of stream and throw error'''
        token: Token | None = self._next()
        # -TODO: Handle errors
        if token is None:
            print(f"Unexpected end of stream, expected '{_type}'")
        elif token.type != _type:
            print(f"Unexpected token '{token.type}', expected '{_type}'")
        return token

    def _check(self, _type: Token.Type) -> bool:
        '''Returns true if current token matches expected type
        or returns false and sets buffer to current token'''
        token: Token | None = self._next()
        if token is None or token.type != _type:
            self._token_buffer = token
            return False
        return True

    def _next(self) -> Token | None:
        '''Read next token from token generator or get current token in buffer'''
        if self._token_buffer:
            token: Token | None = self._token_buffer
            self._token_buffer = None
            return token
        return next(self._token_generator, None)

    def _peek(self) -> Token | None:
        '''Return next token while setting buffer to token'''
        token: Token | None = self._next()
        self._token_buffer = token
        return token

    # -Instance Methods: Parsing
    def _parse_statement(self) -> Node:
        '''PARSE: STATEMENT
        statement: expression ';'
        '''
        debug_print: bool = self._check(Token.Type.IDENTIFIER)
        if debug_print:
            self._advance(Token.Type.LPAREN)
        statement: Node = self._parse_expression()
        if debug_print:
            self._advance(Token.Type.RPAREN)
            statement = CallNode(statement)
        self._advance(Token.Type.SEMICOLON)
        return statement

    def _parse_expression(self) -> Node:
        '''PARSE: EXPRESSION
        expression: expression_term
        '''
        return self._parse_expression_term()

    def _parse_expression_term(self) -> Node:
        '''PARSE: EXPRESSION TERM
        expression_term: expression_factor (('+' | '-') expression_factor)*
        '''
        expr = self._parse_expression_factor()
        while cast(Token, self._peek()).type in (
            Token.Type.ADD, Token.Type.SUB
        ):
            token: Token = cast(Token, self._next())
            rhs = self._parse_expression_factor()
            expr = ExpressionNode(EXPRESSIONS[token.type], expr, rhs)
        return expr

    def _parse_expression_factor(self) -> Node:
        '''PARSE: EXPRESSION FACTOR
        expression_factor: expression_primary (('*' | '/' | '%') expression_primary)*
        '''
        expr = self._parse_expression_primary()
        while cast(Token, self._peek()).type in (
            Token.Type.MUL, Token.Type.DIV, Token.Type.MOD
        ):
            token: Token = cast(Token, self._next())
            rhs = self._parse_literal_numeric()
            expr = ExpressionNode(EXPRESSIONS[token.type], expr, rhs)
        return expr

    def _parse_expression_primary(self) -> Node:
        '''PARSE: EXRESSION PRIMARY
        expression_primary: LITERAL_NUMERIC | '(' expression ')'
        '''
        if self._check(Token.Type.LPAREN):
            expr: Node = self._parse_expression()
            self._advance(Token.Type.RPAREN)
            return expr
        return self._parse_literal_numeric()

    def _parse_literal_numeric(self) -> ValueNode:
        '''PARSE: LITERAL NUMERIC'''
        negate: bool = self._check(Token.Type.SUB)
        token: Token = cast(Token, self._advance(Token.Type.NUMERIC))
        return ValueNode(
            ValueNode.Type.NUMERIC, ('-' if negate else '') + cast(str, token.value)
        )

    # -Instance Methods: Public
    def parse(self) -> list[Node]:
        '''Return abstract-syntax tree from token generator assigned to parser on creation'''
        nodes: list[Node] = []
        while self._peek():
            node: Node = self._parse_statement()
            nodes.append(node)
        return nodes

    # -Class Methods
    @classmethod
    def from_lexer(cls, lexer: Lexer) -> Parser:
        '''Create parser from lexer and assign token generator to parser'''
        return cls(lexer.token_generator)

    @classmethod
    def from_list(cls, tokens: list[Token]) -> Parser:
        '''Create parser from list of tokens and create token generator for parser'''
        return cls(iter(tokens))
