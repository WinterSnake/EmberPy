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
from .token import Token, get_token_representation
from ..errors import DebugLevel, EmberError
from ..location import Location
from ..middleware.nodes import (
    LITERAL,
    Node, NodeExpr,
    NodeDeclModule,
    NodeStmtExpression,
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

    def _error(
            self, code: int, location: Location | None = None, **kwargs: Any
    ) -> EmberError:
        if location is None:
            location = self._last_token.location
        err = EmberError(code, location, **kwargs)
        self.errors.append(err)
        return err

    def _sync(self) -> None:
        while token := self._advance():
            if token.type is Token.Type.SymbolSemicolon:
                break

    # -Instance Methods: Parse
    def parse(self) -> Node:
        '''
        Grammar[Module]
        statement*;
        '''
        nodes: list[Node] = []
        while self._peek():
            node = self._parse_statement()
            if isinstance(node, Node):
                nodes.append(node)
                continue
            # -Error Recovery
            self._sync()
        return NodeDeclModule(nodes)

    def _parse_statement(self) -> Node | EmberError:
        '''
        Grammar[Statement]
        statement_expression;
        '''
        return self._parse_statement_expression()

    def _parse_statement_expression(self) -> Node | EmberError:
        '''
        Grammar[Statement::Expression]
        expression ';';
        '''
        expression = self._parse_expression()
        if isinstance(expression, EmberError):
            return expression
        if not self._consume(Token.Type.SymbolSemicolon):
            code: int = EmberError.invalid_consume_symbol
            if self.is_at_end:
                code = EmberError.invalid_consume_symbol_eof
            self._error(code, symbol=';')
        return NodeStmtExpression(expression)

    def _parse_expression(self) -> NodeExpr | EmberError:
        '''
        Grammar[Expression]
        expression_binary;
        '''
        return self._parse_expression_binary()

    def _parse_expression_binary(self) -> NodeExpr | EmberError:
        '''
        Grammar[Expression::Binary]
        expression_literal ( ('+' | '-' | '*' | '/' | '%') expression_literal)*;
        '''
        # -Internal Functions
        def _term() -> NodeExpr | EmberError:
            '''
            Grammar[Expression::Binary::Term]
            factor ( ('+' | '-') factor)*;
            '''
            if self.debug_level <= DebugLevel.Info:
                print(f"[Parser::Expression::Binary::Term]")
            lhs = _factor()
            if isinstance(lhs, EmberError):
                return lhs
            while token := self._match(
                Token.Type.SymbolPlus,
                Token.Type.SymbolMinus,
            ):
                operator = OPERATOR_BINARY[token.type]
                rhs = _factor()
                if isinstance(rhs, EmberError):
                    return rhs
                lhs = NodeExprBinary(token.location, operator, lhs, rhs)
            return lhs

        def _factor() -> NodeExpr | EmberError:
            '''
            Grammar[Expression::Binary::Factor]
            expression_literal ( ('*' | '/' | '%') expression_literal)*;
            '''
            if self.debug_level <= DebugLevel.Info:
                print(f"[Parser::Expression::Binary::Factor]")
            lhs = self._parse_expression_literal()
            if isinstance(lhs, EmberError):
                return lhs
            while token := self._match(
                Token.Type.SymbolStar,
                Token.Type.SymbolFSlash,
                Token.Type.SymbolPercent,
            ):
                operator = OPERATOR_BINARY[token.type]
                rhs = self._parse_expression_literal()
                if isinstance(rhs, EmberError):
                    return rhs
                lhs = NodeExprBinary(token.location, operator, lhs, rhs)
            return lhs
        # -Body
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Expression::Binary]")
        return _term()

    def _parse_expression_literal(self) -> NodeExpr | EmberError:
        '''
        Grammar[Expression::Literal]
        NUMBER;
        '''
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Expression::Literal]")
        literal = self._advance()
        if literal is None:
            return self._error(EmberError.invalid_expression_eof)
        _type: NodeExprLiteral.Type
        value: LITERAL
        match literal.type:
            case Token.Type.Integer:
                _type = NodeExprLiteral.Type.Integer
                value = int(literal.value)
            case _:
                self._buffer = literal
                return self._error(
                    EmberError.invalid_expression,
                    literal.location,
                    value=get_token_representation(literal),
                )
        return NodeExprLiteral(literal.location, _type, value)

    # -Properties
    @property
    def has_error(self) -> bool:
        return len(self.errors) > 0
