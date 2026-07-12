##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Parser              ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING, Self, cast
from .token import Token
from ..core import LookaheadBuffer, Span
from ..ast import (
    AssignOperator,
    BinaryOperator,
    UnresolvedNode,
    UnresolvedTypeNode,
    UnresolvedUnitNode,
    UnresolvedVariableNode,
    UnresolvedExprNode,
    UnresolvedGroupNode,
    UnresolvedAssignNode,
    UnresolvedBinaryNode,
    UnresolvedLiteralNode,
    UnresolvedIdentifierNode,
)

if TYPE_CHECKING:
    from collections.abc import Iterator
    from .lexer import Lexer
    from ..diagnostics import DiagnosticEngine

## Constants
TYPES = {
    Token.Kind.KeywordInt32: UnresolvedTypeNode.Kind.Int32,
}
LITERALS = (
    Token.Kind.Identifier,
    Token.Kind.Integer,
)
BINARY_OPERATORS = {
    Token.Kind.SymbolPlus: (BinaryOperator.Add, 1),
    Token.Kind.SymbolMinus: (BinaryOperator.Sub, 1),
    Token.Kind.SymbolStar: (BinaryOperator.Mul, 2),
    Token.Kind.SymbolFSlash: (BinaryOperator.Div, 2),
    Token.Kind.SymbolPercent: (BinaryOperator.Mod, 2),
}
ASSIGNMENT_OPERATORS = {
    Token.Kind.SymbolEq: AssignOperator.Eq,
}
STATEMENT_STARTERS = (
    Token.Kind.SymbolSemicolon,
)


## Classes
class Parser(LookaheadBuffer[Token, Token.Kind]):
    """
    Ember Lookahead(n) Parser

    Consumes a stream of tokens from a lookahead buffer and applies a top-down,
    recursive descent strategy to generate an unresolved AST.
    Tracks source locations and integrates with a diagnostic engine for error reporting
    """

    # -Constructor
    def __init__(
        self, _id: int, source: Iterator[Token], engine: DiagnosticEngine
    ) -> None:
        super().__init__(source, lambda token: token.kind)
        # -Location
        self.id: int = _id
        self._last_token: Token | None = None
        # -Diagnostics
        self._engine: DiagnosticEngine = engine

    # -Instance Methods: Lookahead
    def advance(self) -> Token | None:
        token = super().advance()
        if token is not None:
            self._last_token = token
        return token

    def requires(self, *expected: Token.Kind) -> Token:
        if self.matches(*expected):
            return self.next()
        # -TODO: Error[syntax] codes
        names = ','.join(kind.name for kind in expected)
        error = f"Expected [{names}] but got"
        if self.is_at_end:
            self._engine.error(f"{error} end of stream")
        else:
            self._engine.error(f"{error} {self.current.kind.name}")
        # -TODO: parser sync error
        raise StopIteration

    # -Instance Methods: Parser
    def parse(self) -> UnresolvedNode:
        '''
        Grammar[Unit]
        declaration*;
        '''
        nodes: list[UnresolvedNode] = []
        first_token = self.peek()
        while not self.is_at_end:
            node = self._parse_declaration()
            nodes.append(node)
        if self._last_token is None:
            span = Span(self.id, 0, 0)
        else:
            first_token = cast(Token, first_token)
            span = self.last_token.span.extend_from(first_token.span)
        return UnresolvedUnitNode(span, nodes)

    def _parse_declaration(self) -> UnresolvedNode:
        '''
        Grammar[Declaration]
        declaration_statement;
        '''
        return self._parse_declaration_statement()

    def _parse_declaration_variable(
        self, _type: UnresolvedNode | None = None
    ) -> UnresolvedNode:
        '''
        Grammar[Declaration:Variable]
        TYPE entry+ ';';
        '''
        # -Internal Methods
        def _parse_entry() -> UnresolvedVariableNode.Entry:
            '''
            Grammar[Entry]
            IDENTIFIER ('=' expression)?;
            '''
            identifier = self.requires(Token.Kind.Identifier)
            name = identifier.value_as(str)
            span = identifier.span
            initializer: UnresolvedNode | None = None
            if self.consume(Token.Kind.SymbolEq):
                initializer = self._parse_expression()
                span = span.extend_to(initializer.wide_span)
            return UnresolvedVariableNode.Entry(span, name, initializer)
        # -Body
        if _type is None:
            _type = self._parse_type()
        entries = [_parse_entry()]
        while self.consume(Token.Kind.SymbolComma):
            entries.append(_parse_entry())
        token = self.requires(Token.Kind.SymbolSemicolon)
        span = _type.location.extend_to(token.span)
        return UnresolvedVariableNode(span, _type, entries)

    def _parse_declaration_statement(self) -> UnresolvedNode:
        '''
        Grammar[Declaration:Statement]
        declaration_variable | statement;
        '''
        if self.matches(*STATEMENT_STARTERS):
            return self._parse_statement()
        is_decl, head = self._try_parse_type()
        if is_decl:
            return self._parse_declaration_variable(head)
        return self._parse_statement_expression(head)

    def _parse_statement(self) -> UnresolvedNode:
        '''
        Grammar[Statement]
        statement_expression;
        '''
        return self._parse_statement_expression()

    def _parse_statement_expression(
        self, expr: UnresolvedNode | None = None
    ) -> UnresolvedNode:
        '''
        Grammar[Statement:Expression]
        expression? ';';
        '''
        if self.consume(Token.Kind.SymbolSemicolon):
            return UnresolvedExprNode(self.last_token.span, expr)
        expr = self._parse_expression(expr)
        token = self.requires(Token.Kind.SymbolSemicolon)
        return UnresolvedExprNode(token.span, expr)

    def _parse_expression(
        self, l_value: UnresolvedNode | None = None
    ) -> UnresolvedNode:
        '''
        Grammar[Expression]
        expression_binary ('=' expression)?;
        '''
        l_value = self._parse_expression_binary(lhs=l_value)
        if self.matches(*ASSIGNMENT_OPERATORS.keys()):
            token = self.next()
            operator = ASSIGNMENT_OPERATORS[token.kind]
            r_value = self._parse_expression()
            l_value = UnresolvedAssignNode(token.span, operator, l_value, r_value)
        return l_value

    def _parse_expression_binary(
        self, current: int = 0, lhs: UnresolvedNode | None = None
    ) -> UnresolvedNode:
        '''
        Grammar[Expression:Binary]
        expression_binary ('*' | '/' | '%') expression_binary |
        expression_binary ('+' | '-') expression_binary |
        expression_primary;
        '''
        if lhs is None:
            lhs = self._parse_expression_primary()
        while self.matches(*BINARY_OPERATORS.keys()):
            token = self.current
            operator, precedence = BINARY_OPERATORS[token.kind] 
            if precedence <= current:
                break
            token = self.next()
            rhs = self._parse_expression_binary(precedence)
            lhs = UnresolvedBinaryNode(token.span, operator, lhs, rhs)
        return lhs

    def _parse_expression_primary(self) -> UnresolvedNode:
        '''
        Grammar[Expression:Primary]
        '(' expression ')' |
        IDENTIFIER |
        INTEGER;
        '''
        # -Group
        if self.consume(Token.Kind.SymbolLParen):
            start = self.last_token
            inner = self._parse_expression()
            end = self.requires(Token.Kind.SymbolRParen)
            span = start.span.extend_to(end.span)
            return UnresolvedGroupNode(span, inner)
        # -Literal
        return self._parse_literal()

    # -Instance Methods: Helpers
    def _parse_literal(self) -> UnresolvedNode:
        '''
        Grammar[Literal]
        TYPE | IDENTIFIER | INTEGER;

        Used as a factory pattern to create concrete types, identifiers, or literals.
        '''
        # -Type
        if self.matches(*TYPES.keys()):
            token = self.next()
            return UnresolvedTypeNode(token.span, TYPES[token.kind])
        # -Literal
        token = self.requires(*LITERALS)
        match token.kind:
            case Token.Kind.Identifier:
                return UnresolvedIdentifierNode(
                    token.span, token.value_as(str)
                )
            case Token.Kind.Integer:
                return UnresolvedLiteralNode.integer(
                    token.span, token.value_as(int)
                )
        assert False, f"Invalid parser state; parse_literal fell through {token}"

    def _parse_type(self) -> UnresolvedNode:
        '''
        Parses a type signature.

        Handles the base type identifier or primitive, along with any modifiers/qualifiers.
        '''
        return self._parse_expression_primary()

    def _try_parse_type(self) -> tuple[bool, UnresolvedNode]:
        '''
        Disambiguates variable declarations from expression statements.
        
        Parses the leading type node and checks for a trailing identifier 
        to confirm a declaration, returning the 'head' node to prevent backtracking.
        '''
        head = self._parse_type()
        is_decl = self.matches(Token.Kind.Identifier)
        return (is_decl, head)

    # -Class Methods
    @classmethod
    def from_lexer(cls, lexer: Lexer) -> Self:
        return cls(lexer.id, lexer, lexer._engine)

    # -Properties
    @property
    def last_token(self) -> Token:
        assert self._last_token is not None
        return self._last_token

    # -Class Properties
    __slots__ = ('id', '_last_token', '_engine')
