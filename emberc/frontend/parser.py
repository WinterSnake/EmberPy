##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Parser                        ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import Any, Iterator
from .lookahead_buffer import LookaheadBuffer
from .token import Token
from ..errors import DebugLevel, EmberError
from ..location import Location
from ..middleware.nodes import (
    LITERAL,
    Node, NodeExpr,
    NodeExprBinary,
    NodeExprLiteral,
)

## Constants
OPERATOR_BINARY: dict[Token.Type, NodeExprBinary.Operator] = {
    Token.Type.SymbolPlus: NodeExprBinary.Operator.Add,
    Token.Type.SymbolMinus: NodeExprBinary.Operator.Sub,
    Token.Type.SymbolStar: NodeExprBinary.Operator.Mul,
    Token.Type.SymbolFSlash: NodeExprBinary.Operator.Div,
    Token.Type.SymbolPercent: NodeExprBinary.Operator.Mod,
}


## Classes
class Parser(LookaheadBuffer[Token, Token.Type]):
    """
    Ember Language Parser
    Lookahead(1)

    Iterates over token stream and produces a given AST node
    where each grammar rule is represented as an internal method.
    """

    # -Constructor
    def __init__(self, iterator: Iterator[Token]) -> None:
        self.debug_level: DebugLevel = DebugLevel.Off
        self.errors: list[EmberError] = []
        # -Lookahead
        self._iterator: Iterator[Token] = iterator
        self._key = lambda token: token.type
        # -State
        self.is_at_end: bool = False
        self._last_token: Token

    # -Instance Methods: Control
    def _next(self) -> Token | None:
        value = next(self._iterator, None)
        if self.debug_level <= DebugLevel.Trace:
            print(f"[Parser::Next] {value}")
        if value is not None:
            self._last_token = value
        else:
            self.is_at_end = True
        return value

    # -Instance Methods: Parse
    def parse(self) -> Node:
        '''
        Grammar[Module]
        expression;
        '''
        return self._parse_expression()

    def _parse_expression(self) -> NodeExpr:
        '''
        Grammar[Expression]
        expression_binary;
        '''
        return self._parse_expression_binary()

    def _parse_expression_binary(self) -> NodeExpr:
        '''
        Grammar[Expression::Binary]
        expression_literal ( ('+' | '-' | '*' | '/' | '%') expression_literal)*;
        '''
        # -Internal Functions
        def _term() -> NodeExpr:
            '''
            Grammar[Expression::Binary::Term]
            factor ( ('+' | '-') factor)*;
            '''
            if self.debug_level <= DebugLevel.Info:
                print(f"[Parser::Expression::Binary::Term]")
            lhs = _factor()
            while token := self._match(
                Token.Type.SymbolPlus,
                Token.Type.SymbolMinus,
            ):
                operator = OPERATOR_BINARY[token.type]
                rhs = _factor()
                lhs = NodeExprBinary(token.location, operator, lhs, rhs)
            return lhs

        def _factor() -> NodeExpr:
            '''
            Grammar[Expression::Binary::Factor]
            expression_literal ( ('*' | '/' | '%') expression_literal)*;
            '''
            if self.debug_level <= DebugLevel.Info:
                print(f"[Parser::Expression::Binary::Factor]")
            lhs = self._parse_expression_literal()
            while token := self._match(
                Token.Type.SymbolStar,
                Token.Type.SymbolFSlash,
                Token.Type.SymbolPercent,
            ):
                operator = OPERATOR_BINARY[token.type]
                rhs = self._parse_expression_literal()
                lhs = NodeExprBinary(token.location, operator, lhs, rhs)
            return lhs
        # -Body
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Expression::Binary]")
        return _term()

    def _parse_expression_literal(self) -> NodeExpr:
        '''
        Grammar[Expression::Literal]
        NUMBER;
        '''
        literal = self._advance()
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Expression::Literal] {literal}")
        # -TODO: Error Handling
        if literal is None:
            assert False
        match literal.type:
            case Token.Type.Integer:
                return NodeExprLiteral(
                    literal.location,
                    NodeExprLiteral.Type.Integer,
                    int(literal.value)
                )
            # -TODO: Error Handling
            case _:
                assert False

    # -Properties
    @property
    def has_error(self) -> bool:
        return len(self.errors) > 0
