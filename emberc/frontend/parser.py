##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Parser                        ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Sequence
from typing import Any, Iterator, Literal
from .lookahead_buffer import LookaheadBuffer
from .token import Token, get_token_repr
from ..errors import DebugLevel, EmberError
from ..location import Location
from ..middleware.nodes import (
    LITERAL,
    Node, NodeExpr,
    NodeDeclModule, NodeDeclFunction, NodeDeclVariable,
    NodeStmtBlock, NodeStmtExpression,
    NodeExprBinary,
    NodeExprGroup, NodeExprVariable, NodeExprLiteral,
)
from ..middleware.symbol_table import SymbolTable

## Constants
TYPES_TABLE: tuple[Token.Type, ...] = (
    Token.Type.KeywordVoid,
    Token.Type.KeywordBoolean,
    Token.Type.KeywordInt8,
    Token.Type.KeywordInt16,
    Token.Type.KeywordInt32,
    Token.Type.KeywordInt64,
    Token.Type.KeywordUInt8,
    Token.Type.KeywordUInt16,
    Token.Type.KeywordUInt32,
    Token.Type.KeywordUInt64,
)
# BINARY_OPERATORS: '+' | '-' | '*' | '/' | '%' | '<' | '>' | '<=' | '>=' | '==' | '!=';
OPERATOR_BINARY_TABLE: dict[Token.Type, NodeExprBinary.Operator] = {
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
        self._table: SymbolTable
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
        if self.debug_level <= DebugLevel.Warn:
            print(f"[Parser::Error] [{location}] {code}")
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
                token = self._peek()
                if token is not None and token.type is Token.Type.SymbolRBrace:
                    _ = self._advance()
                break

    # -Instance Methods: Parse
    def parse(self, table: SymbolTable) -> Node:
        '''
        Grammar[Module]
        declaration*;
        '''
        self._table = table
        nodes: list[Node] = []
        while token := self._peek():
            if self.debug_level <= DebugLevel.Trace:
                print(f"[Parser::Iter]{token}")
            node = self._parse_declaration()
            # -Error Recovery
            if isinstance(node, EmberError):
                self._sync()
            else:
                nodes.append(node)
        return NodeDeclModule(nodes)

    def _parse_declaration(self) -> Node | EmberError:
        '''
        Grammar[Declaration]
        declaration_function | statement;
        '''
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Declaration]")
        # -Rule: Function Declaration
        if self._consume(Token.Type.KeywordFunction):
            return self._parse_declaration_function()
        # -Rule: Statement
        return self._parse_statement()

    def _parse_declaration_function(self) -> Node | EmberError:
        '''
        Grammar[Declaration::Function]
        'fn' IDENTIFIER '(' ')' ':' TYPE '{' statement* '}';
        '''
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Declaration::Function]")
        _id = self._advance()
        # -Invalid Identifier consume (end of stream)
        if _id is None:
            return self._error(EmberError.invalid_identifier_eof)
        # -Invalid Identifier consume
        elif _id.type is not Token.Type.Identifier:
            return self._error(
                EmberError.invalid_identifier,
                value=get_token_repr(_id)
            )
        entry: int = self._table.add(_id.value)
        if not self._consume(Token.Type.SymbolLParen):
            return self._error(EmberError.invalid_consume_symbol, symbol='(')
        if not self._consume(Token.Type.SymbolRParen):
            return self._error(EmberError.invalid_consume_symbol, symbol=')')
        if not self._consume(Token.Type.SymbolColon):
            return self._error(EmberError.invalid_consume_symbol, symbol=':')
        _type: Token | Literal[False]
        # -Invalid type
        if not (_type := self._match(*TYPES_TABLE)):
            if self.is_at_end:
                return self._error(EmberError.invalid_type_eof)
            else:
                assert not isinstance(_type, bool)
                return self._error(
                    EmberError.invalid_type,
                    _type.location,
                    value=get_token_repr(_type),
                )
        if not self._consume(Token.Type.SymbolLBrace):
            return self._error(EmberError.invalid_consume_symbol, symbol='{')
        body = self._parse_statement_block()
        return NodeDeclFunction(entry, body)

    def _parse_declaration_variable(self, type_token: Token) -> Node | EmberError:
        '''
        Grammar[Declaration::Variable]
        TYPE IDENTIFIER ('=' expression)? ';';
        '''
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Declaration::Variable]")
        _id = self._advance()
        # -Invalid Identifier consume (end of stream)
        if _id is None:
            return self._error(EmberError.invalid_identifier_eof)
        # -Invalid Identifier consume
        elif _id.type is not Token.Type.Identifier:
            return self._error(
                EmberError.invalid_identifier,
                value=get_token_repr(_id)
            )
        entry: int = self._table.add(_id.value)
        initializer: NodeExpr | None = None
        if self._consume(Token.Type.SymbolEq):
            _initializer = self._parse_expression()
            if isinstance(_initializer, EmberError):
                return _initializer
            initializer = _initializer
        # --Invalid ';' consume
        if not self._consume(Token.Type.SymbolSemicolon):
            _ = self._error(EmberError.invalid_consume_symbol, symbol=';')
        return NodeDeclVariable(entry, initializer)

    def _parse_statement(self) -> Node | EmberError:
        '''
        Grammar[Statement]
        declaration_variable | statement_block | statement_expression;
        '''
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Statement]")
        # -Rule: Variable Declaration
        if token := self._match(*TYPES_TABLE):
            return self._parse_declaration_variable(token)
        # -Rule: Block
        elif self._consume(Token.Type.SymbolLBrace):
            body = self._parse_statement_block()
            return NodeStmtBlock(body)
        # -Rule: Expression
        return self._parse_statement_expression()

    def _parse_statement_block(self) -> Sequence[Node]:
        '''
        Grammar[Statement::Block]
        '{' statement* '}';
        '''
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Statement::Block]")
        nodes: list[Node] = []
        while not self._consume(Token.Type.SymbolRBrace):
            # --Invalid '}' consume
            if self.is_at_end:
                _ = self._error(EmberError.invalid_consume_symbol, symbol='}')
            node = self._parse_statement()
            # -Error Recovery
            if isinstance(node, EmberError):
                self._sync()
            else:
                nodes.append(node)
        return nodes

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
            _ = self._error(EmberError.invalid_consume_symbol, symbol=';')
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
                operator = OPERATOR_BINARY_TABLE[token.type]
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
                operator = OPERATOR_BINARY_TABLE[token.type]
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
                operator = OPERATOR_BINARY_TABLE[token.type]
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
                operator = OPERATOR_BINARY_TABLE[token.type]
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
        IDENTIFIER | BOOLEAN | NUMBER | '(' expression ')';
        '''
        if self.debug_level <= DebugLevel.Info:
            print(f"[Parser::Expression::Primary]")
        # -Rule: Group
        if self._consume(Token.Type.SymbolLParen):
            node = self._parse_expression()
            if isinstance(node, EmberError):
                return node
            # -Invalid ')' consume
            if not self._consume(Token.Type.SymbolRParen):
                _ = self._error(EmberError.invalid_consume_symbol, symbol=')')
            return NodeExprGroup(node)
        # -Rule: Literal
        _type: NodeExprLiteral.Type
        value: LITERAL
        literal = self._advance()
        # -Invalid expression consume (end of stream)
        if literal is None:
            return self._error(EmberError.invalid_expression_eof)
        match literal.type:
            case Token.Type.Identifier:
                entry: int = self._table.get(literal.value)
                return NodeExprVariable(literal.location, entry)
            case Token.Type.KeywordTrue:
                _type = NodeExprLiteral.Type.Boolean
                value = True
            case Token.Type.KeywordFalse:
                _type = NodeExprLiteral.Type.Boolean
                value = False
            case Token.Type.Integer:
                _type = NodeExprLiteral.Type.Integer
                value = int(literal.value)
            # -Invalid expression consume
            case _:
                self._buffer = literal
                return self._error(
                    EmberError.invalid_expression,
                    literal.location,
                    value=get_token_repr(literal),
                )
        return NodeExprLiteral(literal.location, _type, value)

    # -Properties
    @property
    def has_error(self) -> bool:
        return len(self.errors) > 0
