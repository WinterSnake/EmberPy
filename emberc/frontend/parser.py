##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Parser                        ##
##-------------------------------##

## Imports
from __future__ import annotations
import sys
from collections.abc import Iterator
from .token import Token
from ..middleware.nodes import (
    Node,
    NodeStatementUnit,
    NodeExprBinary, NodeExprUnary, NodeExprGroup, NodeExprLiteral
)

## Constants
OPERATOR_BINARY: dict[Token.Type, NodeExprBinary.Type] = {
    Token.Type.Plus: NodeExprBinary.Type.Add,
    Token.Type.Minus: NodeExprBinary.Type.Sub,
    Token.Type.Star: NodeExprBinary.Type.Mul,
    Token.Type.FSlash: NodeExprBinary.Type.Div,
    Token.Type.Percent: NodeExprBinary.Type.Mod,
}
OPERATOR_UNARY: dict[Token.Type, NodeExprUnary.Type] = {
    Token.Type.Minus: NodeExprUnary.Type.Negative,
}


## Classes
class Parser:
    """
    Ember Parser
    Lookahead(1)
    """

    # -Constructor
    def __init__(self, token_iter: Iterator[Token]) -> None:
        self.is_at_end: bool = False
        self._token_iter: Iterator[Token] = token_iter
        self._lookahead: Token | None = None
        self._last_token: Token = None  # type: ignore

    # -Instance Methods: Control
    def _next(self) -> Token | None:
        '''Returns token from iterator or inner buffer'''
        token: Token | None
        if self._lookahead:
            token = self._lookahead
            self._lookahead = None
            return token
        token = next(self._token_iter, None)
        if token is None:
            self.is_at_end = True
        else:
            self._last_token = token
        return token

    def _peek(self) -> Token | None:
        '''Retrieves next token and sets inner buffer'''
        token = self._next()
        self._lookahead = token
        return token

    def _consume(self, _type: Token.Type) -> bool:
        '''Consumes next token if expected type'''
        token = self._peek()
        if token is None or token.type != _type:
            return False
        self._lookahead = None
        return True

    def _match(self, *types: Token.Type) -> Token | None:
        '''Returns next token if token matches expected type'''
        token = self._peek()
        if token is not None and token.type in types:
            return self._next()
        return None

    # -Instance Methods: Parsing
    def parse(self) -> Node:
        '''Produces an AST from a given token iterator and returns any errors encountered'''
        return self._parse_unit()

    def _parse_unit(self) -> Node:
        '''
        Grammar[Unit]
        statement*;
        '''
        token = self._peek()
        # -TODO: Error Handling
        assert token is not None
        nodes: list[Node] = []
        while not self.is_at_end:
            if self._peek() is None:
                break
            node = self._parse_statement()
            nodes.append(node)
        return NodeStatementUnit(token.location.file, nodes)
    
    def _parse_statement(self) -> Node:
        '''
        Grammar[Statement]
        expression ';';
        '''
        node = self._parse_expression()
        # -TODO: Error Handling
        if not self._consume(Token.Type.Semicolon):
            pass
        return node

    def _parse_expression(self) -> Node:
        '''
        Grammar[Expression]
        expression_binary;
        '''
        return self._parse_expression_binary()

    def _parse_expression_binary(self) -> Node:
        '''
        Grammar[Expression::Binary]
        expression_binary_term;
        '''
        return self._parse_expression_binary_term()

    def _parse_expression_binary_term(self) -> Node:
        '''
        Grammar[Expression::Binary::Term]
        expression_binary_factor ( ('+' | '-') expression_binary_factor)*;
        '''
        node = self._parse_expression_binary_factor()
        while (token := self._match(Token.Type.Plus, Token.Type.Minus)):
            operator = OPERATOR_BINARY[token.type]
            rhs = self._parse_expression_unary()
            node = NodeExprBinary(token.location, operator, node, rhs)
        return node

    def _parse_expression_binary_factor(self) -> Node:
        '''
        Grammar[Expression::Binary::Factor]
        expression_unary ( ('*' | '/' | '%') expression_unary)*;
        '''
        node = self._parse_expression_unary()
        while (token := self._match(
            Token.Type.Star, Token.Type.FSlash, Token.Type.Percent
        )):
            operator = OPERATOR_BINARY[token.type]
            rhs = self._parse_expression_unary()
            node = NodeExprBinary(token.location, operator, node, rhs)
        return node

    def _parse_expression_unary(self) -> Node:
        '''
        Grammar[Expression::Unary]
        ('-' unary) | primary;
        '''
        if (token := self._match(Token.Type.Minus)):
            operator = OPERATOR_UNARY[token.type]
            node = self._parse_expression_unary()
            return NodeExprUnary(token.location, operator, node)
        return self._parse_primary()

    def _parse_primary(self) -> Node:
        '''
        Grammar[Expression::Primary]
        expression_literal | '(' expression ')';
        '''
        if self._consume(Token.Type.LParen):
            location = self._last_token.location
            node = self._parse_expression()
            # -TODO: Error Handling
            if not self._consume(Token.Type.RParen):
                pass
            return NodeExprGroup(location, node)
        return self._parse_literal()

    def _parse_literal(self) -> Node:
        '''
        Grammar[Expression::Literal]
        NUMBER;
        '''
        token = self._next()
        assert token is not None
        assert token.value is not None
        assert token.type is Token.Type.Integer
        return NodeExprLiteral(
            token.location, NodeExprLiteral.Type.Integer, int(token.value)
        )
