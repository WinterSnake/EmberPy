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
from .token import Token, get_token_repr
from ..errors import DebugLevel, EmberError
from ..location import Location
from ..middleware.nodes import (
    LITERAL,
    Node, NodeExpr,
    NodeDeclModule, NodeDeclVariable,
    NodeStmtAssignment, NodeStmtExpression,
    NodeExprBinary,
    NodeExprGroup, NodeExprVariable, NodeExprLiteral,
)

## Constants
TYPES_TABLE: tuple[Token.Type, ...] = (
    Token.Type.KeywordInt8,
)
OPERATOR_BINARY: dict[Token.Type, NodeExprBinary.Operator] = {
    # -Math
    Token.Type.SymbolPlus: NodeExprBinary.Operator.Add,
    Token.Type.SymbolMinus: NodeExprBinary.Operator.Sub,
    Token.Type.SymbolStar: NodeExprBinary.Operator.Mul,
    Token.Type.SymbolFSlash: NodeExprBinary.Operator.Div,
    Token.Type.SymbolPercent: NodeExprBinary.Operator.Mod,
    # -Comparisons
    Token.Type.SymbolLt: NodeExprBinary.Operator.Lt,
    Token.Type.SymbolGt: NodeExprBinary.Operator.Gt,
    Token.Type.SymbolLtEq: NodeExprBinary.Operator.LtEq,
    Token.Type.SymbolGtEq: NodeExprBinary.Operator.GtEq,
    Token.Type.SymbolEqEq: NodeExprBinary.Operator.EqEq,
    Token.Type.SymbolBangEq: NodeExprBinary.Operator.NtEq,
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
        if self.debug_level <= DebugLevel.Warn:
            print(f"[Parser::Error] [{location}] {code}")
        if location is None:
            location = self._last_token.location
        err = EmberError(code, location, **kwargs)
        self.errors.append(err)
        return err

    def _sync(self) -> None:
        if self.debug_level <= DebugLevel.Warn:
            print(f"[Parser::Sync]")
        while token := self._advance():
            if self.debug_level <= DebugLevel.Trace:
                print(f"[Parser::Sync::Iter] {token}")
            if token.type is Token.Type.SymbolSemicolon:
                break

    # -Instance Methods: Parse
    def parse(self) -> Node:
        '''
        Grammar[Module]
        statement*;
        '''
        nodes: list[Node] = []
        while token := self._peek():
            if self.debug_level <= DebugLevel.Trace:
                print(f"[[Parser::Iter]{token}")
            node = self._parse_statement()
            if isinstance(node, Node):
                nodes.append(node)
                continue
            # -Error Recovery
            self._sync()
        return NodeDeclModule(nodes)

    def _parse_declaration_variable(self) -> Node | EmberError:
        '''
        Grammar[Declaration::Variable]
        TYPE IDENTIFIER ('=' expression)? ';';
        '''
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Declaration::Variable]")
        _type = self._last_token
        _id = self._advance()
        if _id is None:
            return self._error(EmberError.invalid_identifier_eof)
        elif _id.type is not Token.Type.Identifier:
            return self._error(
                EmberError.invalid_identifier,
                value=get_token_repr(_id)
            )
        initializer: NodeExpr | EmberError | None = None
        if self._consume(Token.Type.SymbolEq):
            initializer = self._parse_expression()
        if isinstance(initializer, EmberError):
            return initializer
        # --Invalid ';' consume
        if not self._consume(Token.Type.SymbolSemicolon):
            code: int = EmberError.invalid_consume_symbol
            if self.is_at_end:
                code = EmberError.invalid_consume_symbol_eof
            _ = self._error(code, symbol=';')
        return NodeDeclVariable(_id.value, initializer)

    def _parse_statement(self) -> Node | EmberError:
        '''
        Grammar[Statement]
        declaration_variable | statement_expression | statement_assignment;
        '''
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Statement]")
        # -Rule: Decl Variable
        if self._match(*TYPES_TABLE):
            return self._parse_declaration_variable()
        # -Rule: Stmt Assignment
        elif self._match(Token.Type.Identifier):
            return self._parse_statement_assignment()
        # -Rule: Stmt Expression
        return self._parse_statement_expression()

    def _parse_statement_assignment(self) -> Node | EmberError:
        '''
        Grammar[Statement::Assignment]
        IDENTIFIER '=' expression ';';
        '''
        _id = self._last_token
        code: int
        # -Invalid '=' consume
        if not self._consume(Token.Type.SymbolEq):
            code = EmberError.invalid_consume_symbol
            if self.is_at_end:
                code = EmberError.invalid_consume_symbol_eof
            return self._error(code, symbol='=')
        expression = self._parse_expression()
        if isinstance(expression, EmberError):
            return expression
        # --Invalid ';' consume
        if not self._consume(Token.Type.SymbolSemicolon):
            code = EmberError.invalid_consume_symbol
            if self.is_at_end:
                code = EmberError.invalid_consume_symbol_eof
            _ = self._error(code, symbol=';')
        return NodeStmtAssignment(_id.value, expression)

    def _parse_statement_expression(self) -> Node | EmberError:
        '''
        Grammar[Statement::Expression]
        expression ';';
        '''
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Statement::Expression]")
        node = self._parse_expression()
        if isinstance(node, EmberError):
            return node
        # --Invalid ';' consume
        if not self._consume(Token.Type.SymbolSemicolon):
            code: int = EmberError.invalid_consume_symbol
            if self.is_at_end:
                code = EmberError.invalid_consume_symbol_eof
            _ = self._error(code, symbol=';')
        return NodeStmtExpression(node)

    def _parse_expression(self) -> NodeExpr | EmberError:
        '''
        Grammar[Expression]
        expression_binary;
        '''
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Expression]")
        return self._parse_expression_binary()

    def _parse_expression_binary(self) -> NodeExpr | EmberError:
        '''
        Grammar[Expression::Binary]
        expression_primary (BINARY_OPERATOR expression_primary)*;
        '''
        # -Internal Functions
        def _equality() -> NodeExpr | EmberError:
            '''
            Grammar[Expression::Binary::Equality]
            comparison ( ('==' | '!=') comparison)*;
            '''
            if self.debug_level <= DebugLevel.Info:
                print(f"[Parser::Expression::Binary::Equality]")
            lhs = _comparison()
            if isinstance(lhs, EmberError):
                return lhs
            while token := self._match(
                Token.Type.SymbolEqEq,
                Token.Type.SymbolBangEq,
            ):
                operator = OPERATOR_BINARY[token.type]
                rhs = _comparison()
                if isinstance(rhs, EmberError):
                    return rhs
                lhs = NodeExprBinary(token.location, operator, lhs, rhs)
            return lhs

        def _comparison() -> NodeExpr | EmberError:
            '''
            Grammar[Expression::Binary::Comparison]
            term ( ('<' | '>' | '<=' | '>=') term)*;
            '''
            if self.debug_level <= DebugLevel.Info:
                print(f"[Parser::Expression::Binary::Comparison]")
            lhs = _term()
            if isinstance(lhs, EmberError):
                return lhs
            while token := self._match(
                Token.Type.SymbolLt,
                Token.Type.SymbolGt,
                Token.Type.SymbolLtEq,
                Token.Type.SymbolGtEq,
            ):
                operator = OPERATOR_BINARY[token.type]
                rhs = _term()
                if isinstance(rhs, EmberError):
                    return rhs
                lhs = NodeExprBinary(token.location, operator, lhs, rhs)
            return lhs

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
            expression_primary ( ('*' | '/' | '%') expression_primary)*;
            '''
            if self.debug_level <= DebugLevel.Info:
                print(f"[Parser::Expression::Binary::Factor]")
            lhs = self._parse_expression_primary()
            if isinstance(lhs, EmberError):
                return lhs
            while token := self._match(
                Token.Type.SymbolStar,
                Token.Type.SymbolFSlash,
                Token.Type.SymbolPercent,
            ):
                operator = OPERATOR_BINARY[token.type]
                rhs = self._parse_expression_primary()
                if isinstance(rhs, EmberError):
                    return rhs
                lhs = NodeExprBinary(token.location, operator, lhs, rhs)
            return lhs
        # -Body
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Expression::Binary]")
        return _equality()

    def _parse_expression_primary(self) -> NodeExpr | EmberError:
        '''
        Grammar[Expression::Primary]
        IDENTIFIER | NUMBER | '(' expression ')';
        '''
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Expression::Primary]")
        # - Rule: Grouping
        code: int
        if self._consume(Token.Type.SymbolLParen):
            node = self._parse_expression()
            if isinstance(node, EmberError):
                return node
            if self._consume(Token.Type.SymbolRParen):
                return NodeExprGroup(node)
            code = EmberError.invalid_consume_symbol
            if self.is_at_end:
                code = EmberError.invalid_consume_symbol_eof
            return self._error(code, symbol=')')
        # - Rule: Literal
        literal = self._advance()
        if literal is None:
            return self._error(EmberError.invalid_expression_eof)
        _type: NodeExprLiteral.Type
        value: LITERAL
        match literal.type:
            case Token.Type.KeywordTrue:
                _type = NodeExprLiteral.Type.Boolean
                value = True
            case Token.Type.KeywordFalse:
                _type = NodeExprLiteral.Type.Boolean
                value = False
            case Token.Type.Integer:
                _type = NodeExprLiteral.Type.Integer
                value = int(literal.value)
            case Token.Type.Identifier:
                return NodeExprVariable(literal.location, literal.value)
            case _:
                self._buffer = literal
                return self._error(
                    EmberError.invalid_expression,
                    literal.location, value=get_token_repr(literal),
                )
        return NodeExprLiteral(literal.location, _type, value)

    # -Properties
    @property
    def has_error(self) -> bool:
        return len(self.errors) > 0
