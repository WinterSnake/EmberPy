##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Parser              ##
##-------------------------------##

## Imports
from typing import (
    TYPE_CHECKING,
    Literal, Self, TypeIs,
    assert_never
)
from .token import Token
from ..ast import (
    AssignOperator,
    BinaryOperator,
    UnaryOperator,
    PrimitiveType,
    # -Types
    UnresolvedTypeNode,
    # -Declarations
    UnresolvedUnitNode,
    UnresolvedVariableNode,
    # -Statements
    UnresolvedBlockNode,
    UnresolvedConditionalNode,
    UnresolvedExpressionNode,
    # -Expressions
    UnresolvedGroupNode,
    UnresolvedAssignNode,
    UnresolvedBinaryNode,
    UnresolvedUnaryPrefixNode,
    UnresolvedBooleanNode,
    UnresolvedIntegerNode,
    UnresolvedIdentifierNode,
)
from ..core import LookaheadBuffer, Span
from ..diagnostics import Diagnostic

if TYPE_CHECKING:
    from collections.abc import Iterator
    from .lexer import Lexer
    from ..ast import UnresolvedNode
    from ..diagnostics import DiagnosticEngine


## Constants
TYPES = {
    Token.Kind.KeywordVoid: PrimitiveType.Void,
    Token.Kind.KeywordBoolean: PrimitiveType.Boolean,
    Token.Kind.KeywordInt8: PrimitiveType.Int8,
    Token.Kind.KeywordInt16: PrimitiveType.Int16,
    Token.Kind.KeywordInt32: PrimitiveType.Int32,
    Token.Kind.KeywordInt64: PrimitiveType.Int64,
    Token.Kind.KeywordUInt8: PrimitiveType.UInt8,
    Token.Kind.KeywordUInt16: PrimitiveType.UInt16,
    Token.Kind.KeywordUInt32: PrimitiveType.UInt32,
    Token.Kind.KeywordUInt64: PrimitiveType.UInt64,
    Token.Kind.KeywordISize: PrimitiveType.ISize,
    Token.Kind.KeywordUSize: PrimitiveType.USize,
}
LITERALS = (
    Token.Kind.Identifier,
    Token.Kind.Boolean,
    Token.Kind.Integer,
)
UNARY_OPERATORS = {
    Token.Kind.SymbolMinus: UnaryOperator.NumNegate,
    Token.Kind.SymbolBang: UnaryOperator.LogNegate,
}
BINARY_OPERATORS = {
    # -Comparisons
    Token.Kind.SymbolEqEq: (BinaryOperator.Eq, 1),
    Token.Kind.SymbolBangEq: (BinaryOperator.NtEq, 1),
    Token.Kind.SymbolLt: (BinaryOperator.Lt, 2),
    Token.Kind.SymbolGt: (BinaryOperator.Gt, 2),
    Token.Kind.SymbolLtEq: (BinaryOperator.LtEq, 2),
    Token.Kind.SymbolGtEq: (BinaryOperator.GtEq, 2),
    # -Math
    Token.Kind.SymbolPlus: (BinaryOperator.Add, 3),
    Token.Kind.SymbolMinus: (BinaryOperator.Sub, 3),
    Token.Kind.SymbolStar: (BinaryOperator.Mul, 4),
    Token.Kind.SymbolFSlash: (BinaryOperator.Div, 4),
    Token.Kind.SymbolPercent: (BinaryOperator.Mod, 4),
}
ASSIGNMENT_OPERATORS = {
    Token.Kind.SymbolEq: AssignOperator.Eq,
}
STATEMENT_STARTERS = (
    Token.Kind.SymbolLBrace,
    Token.Kind.KeywordIf,
)
type LITERAL_KIND = Literal[
    Token.Kind.Identifier,
    Token.Kind.Boolean,
    Token.Kind.Integer,
]


## Functions
def _is_literal_kind(kind: Token.Kind) -> TypeIs[LITERAL_KIND]:
    return kind in LITERALS


## Classes
class ParserSyncError(BaseException):
    """Thrown to allow parser to sync at boundries; hold diagnostic context."""
    # -Constructor
    def __init__(self, diagnostic: Diagnostic) -> None:
        self.diagnostic = diagnostic

    # -Class Methods
    @classmethod
    def build(cls, code: Diagnostic.Code, span: Span) -> Self:
        return cls(Diagnostic(Diagnostic.Level.Error, code, span))


class Parser(LookaheadBuffer[Token, Token.Kind]):
    """
    Ember Recursive Descent Parser [LL(n)]

    Transform a token source stream into an unresolved AST.
    Attach token spans to corresponding AST nodes and handle
    diagnostic reporting through the engine.
    """
    # -Constructor
    def __init__(
        self, _id: int, source: Iterator[Token], engine: DiagnosticEngine
    ) -> None:
        super().__init__(source, lambda token: token.kind)
        self.id = _id
        self.engine = engine
        self._last_token: Token | None = None

    # -Instance Methods: Lookahead
    def advance(self) -> Token | None:
        '''Advance the stream by one and update last token; return token or None if at end.'''
        if (token := super().advance()) is not None:
            self._last_token = token
        return token

    def requires(
        self, code: Diagnostic.Code,
        *expected: Token.Kind,
        is_delimiter: bool = False,
    ) -> Token:
        '''Return next token if tag matches expected; log error and raise parser sync if not.'''
        if self.matches(*expected):
            return self.next()
        span: Span
        if is_delimiter or self.is_at_end:
            span = Span.point(self.id, self.last_token.span.end)
        else:
            span = self.current.span
        raise ParserSyncError.build(code, span)

    # -Instance Methods: Parsing
    def _sync(self, diagnostic: Diagnostic, consume_block: bool) -> None:
        '''Skip tokens until state boundary is reached, then return control flow.'''
        self.engine.report(diagnostic)
        while token := self.peek():
            match token.kind:
                case Token.Kind.KeywordIf:
                    break
                case Token.Kind.SymbolRBrace:
                    if consume_block:
                        _ = self.advance()
                    break
                case Token.Kind.SymbolSemicolon:
                    _ = self.advance()
                    break
                case _:
                    self.advance()

    def parse(self) -> UnresolvedUnitNode:
        '''
        Grammar[Unit]
        declaration*;
        '''
        nodes: list[UnresolvedNode] = []
        _first_token = self.peek()
        while not self.is_at_end:
            try:
                node = self._parse_declaration()
                nodes.append(node)
            except ParserSyncError as e:
                self._sync(e.diagnostic, True)
        span: Span
        if _first_token is None:
            span = Span(self.id, 0, 0)
        else:
            span = _first_token.span.extend_to(self.last_token.span)
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
        Grammar[Declaration::Variable]
        TYPE entry (',' entry)* ';';
        '''
        # -Internal Functions
        def _parse_entry() -> UnresolvedVariableNode.Entry:
            '''
            Grammar[Declaration::Variable::Entry]
            IDENTIFIER ('=' expression)?;
            '''
            token = self.requires(Diagnostic.Code.E2001, Token.Kind.Identifier)
            initializer: UnresolvedNode | None = None
            span = token.span
            if self.consume(Token.Kind.SymbolEq):
                span = span.extend_to(self.last_token.span)
                initializer = self._parse_expression()
            return UnresolvedVariableNode.Entry(
                span, token.value_as(str), initializer
            )
        # -Body
        if _type is None:
            _type = self._parse_type()
        entries = [_parse_entry()]
        while self.consume(Token.Kind.SymbolComma):
            entries.append(_parse_entry())
        token = self.requires(
            Diagnostic.Code.E2101,
            Token.Kind.SymbolSemicolon,
            is_delimiter=True
        )
        span = entries[0].location.extend_to(token.span)
        return UnresolvedVariableNode(span, _type, entries)

    def _parse_declaration_statement(self) -> UnresolvedNode:
        '''
        Grammar[Declaration::Statement]
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
        statement_block |
        statment_condition |
        statement_expression;
        '''
        if self.matches(Token.Kind.SymbolLBrace):
            return self._parse_statement_block()
        elif self.matches(Token.Kind.KeywordIf):
            return self._parse_statement_condition()
        return self._parse_statement_expression()

    def _parse_statement_block(self) -> UnresolvedNode:
        '''
        Grammar[Statement::Block]
        '{' declaration_statement* '}';
        '''
        assert self.consume(Token.Kind.SymbolLBrace)
        start = self.last_token
        nodes: list[UnresolvedNode] = []
        while not self.matches(Token.Kind.SymbolRBrace) and not self.is_at_end:
            try:
                node = self._parse_declaration_statement()
                nodes.append(node)
            except ParserSyncError as e:
                self._sync(e.diagnostic, False)
        end = self.requires(
            Diagnostic.Code.E2103,
            Token.Kind.SymbolRBrace,
            is_delimiter=True
        )
        span = start.span.extend_to(end.span)
        return UnresolvedBlockNode(span, nodes)

    def _parse_statement_condition(self) -> UnresolvedNode:
        '''
        Grammar[Statement::Condition]
        'if' '(' expression ')' statement ('else' statement)?;
        '''
        assert self.consume(Token.Kind.KeywordIf)
        start = self.last_token
        _ = self.requires(Diagnostic.Code.E2003, Token.Kind.SymbolLParen)
        condition = self._parse_expression()
        _ = self.requires(
            Diagnostic.Code.E2102,
            Token.Kind.SymbolRParen,
            is_delimiter=True
        )
        then_branch = self._parse_statement()
        else_branch: UnresolvedNode | None = None
        if self.consume(Token.Kind.KeywordElse):
            else_branch = self._parse_statement()
        span = start.span.extend_to(self.last_token.span)
        return UnresolvedConditionalNode(
            span, condition, then_branch, else_branch
        )

    def _parse_statement_expression(
        self, expr: UnresolvedNode | None = None
    ) -> UnresolvedNode:
        '''
        Grammar[Statement::Expression]
        expression ';';
        '''
        if expr is not None and self.consume(Token.Kind.SymbolSemicolon):
                span = self.last_token.span.extend_from(expr.wide_span)
                return UnresolvedExpressionNode(span, expr)
        expr = self._parse_expression(expr)
        token = self.requires(
            Diagnostic.Code.E2101,
            Token.Kind.SymbolSemicolon,
            is_delimiter=True
        )
        span = token.span.extend_from(expr.wide_span)
        return UnresolvedExpressionNode(span, expr)

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
            l_value = UnresolvedAssignNode(
                token.span, operator, l_value, r_value
            )
        return l_value

    def _parse_expression_binary(
        self, current: int = 0, lhs: UnresolvedNode | None = None
    ) -> UnresolvedNode:
        '''
        Grammar[Expression::Binary]
        expression_binary ("==" | "!=") expression_binary |
        expression_binary ('<' | "<=" | '>' | ">=") expression_binary |
        expression_binary ('*' | '/' | '%') expression_binary |
        expression_binary ('+' | '-') expression_binary |
        expression_unary;
        '''
        if lhs is None:
            lhs = self._parse_expression_unary_prefix()
        while self.matches(*BINARY_OPERATORS.keys()):
            token = self.current
            operator, precedence = BINARY_OPERATORS[token.kind] 
            if precedence <= current:
                break
            token = self.next()
            rhs = self._parse_expression_binary(precedence)
            lhs = UnresolvedBinaryNode(token.span, operator, lhs, rhs)
        return lhs

    def _parse_expression_unary_prefix(self) -> UnresolvedNode:
        '''
        Grammar[Expression::Unary]
        ('-' | '!') expression_unary |
        expression_primary;
        '''
        if self.matches(*UNARY_OPERATORS.keys()):
            token = self.next()
            operator = UNARY_OPERATORS[token.kind]
            operand = self._parse_expression_unary_prefix()
            return UnresolvedUnaryPrefixNode(token.span, operator, operand)
        return self._parse_expression_primary()

    def _parse_expression_primary(self) -> UnresolvedNode:
        '''
        Grammar[Expression::Primary]
        '(' expression ')' |
        IDENTIFIER | BOOLEAN | INTEGER;
        '''
        # -Group
        if self.consume(Token.Kind.SymbolLParen):
            start = self.last_token
            inner = self._parse_expression()
            end = self.requires(
                Diagnostic.Code.E2102,
                Token.Kind.SymbolRParen,
                is_delimiter=True
            )
            return UnresolvedGroupNode(start.span.extend_to(end.span), inner)
        # -Literal
        return self._parse_literal()

    # -Instance Methods: Helpers
    def _parse_literal(self) -> UnresolvedNode:
        '''
        Grammar[Literal]
        TYPE | IDENTIFIER | BOOLEAN | INTEGER;
        '''
        # -Type
        if self.matches(*TYPES.keys()):
            token = self.next()
            return UnresolvedTypeNode(token.span, TYPES[token.kind])
        # -Literals
        token = self.requires(Diagnostic.Code.E2002, *LITERALS)
        assert _is_literal_kind(token.kind)
        match token.kind:
            case Token.Kind.Identifier:
                return UnresolvedIdentifierNode(token.span, token.value_as(str))
            case Token.Kind.Boolean:
                return UnresolvedBooleanNode(token.span, token.value_as(bool))
            case Token.Kind.Integer:
                return UnresolvedIntegerNode(token.span, token.value_as(int))
            case _:
                assert_never(token.kind)

    def _parse_type(self) -> UnresolvedNode:
        '''Parse a valid type signature; alias for unary expression.'''
        return self._parse_expression_unary_prefix()

    def _try_parse_type(self) -> tuple[bool, UnresolvedNode]:
        '''Try to parse a type signature and return if the signature is followed by an identifier.'''
        head = self._parse_type()
        is_decl = self.matches(Token.Kind.Identifier)
        return (is_decl, head)

    # -Class Methods
    @classmethod
    def from_lexer(cls, lexer: Lexer) -> Self:
        '''Create parser from the given lexer by copying the id and engine.'''
        return cls(lexer.id, lexer.get_token_iter(), lexer.engine)

    # -Properties
    @property
    def last_token(self) -> Token:
        assert self._last_token is not None
        return self._last_token

    # -Class Properties
    __slots__ = (
        "id",
        "engine",
        "_last_token",
    )
