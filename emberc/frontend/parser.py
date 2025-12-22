##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Parser              ##
##-------------------------------##

## Imports
from collections.abc import Iterator
from typing import cast
from .lookahead_buffer import LookaheadBuffer
from .token import Token
from ..errors import EmberError, EmberParserError
from ..middleware.nodes import (
    NODE_TYPE, LITERAL_VALUE,
    NodeBase, NodeType, NodeDecl, NodeStmt, NodeExpr,
    NodeTypeBuiltin, NodeTypeIdentifier,
    NodeDeclUnit, NodeDeclVariable,
    NodeStmtBlock, NodeStmtConditional, NodeStmtLoop, NodeStmtExpression,
    NodeExprAssignment, NodeExprGroup, NodeExprBinary, NodeExprUnary,
    NodeExprVariable, NodeExprLiteral,
)

## Constants
BINARY_OPERATOR = {
    Token.Type.SymbolEqEq: (NodeExprBinary.Operator.EqEq, 1),
    Token.Type.SymbolNtEq: (NodeExprBinary.Operator.NtEq, 1),
    Token.Type.SymbolLt: (NodeExprBinary.Operator.Lt, 2),
    Token.Type.SymbolGt: (NodeExprBinary.Operator.Gt, 2),
    Token.Type.SymbolLtEq: (NodeExprBinary.Operator.LtEq, 2),
    Token.Type.SymbolGtEq: (NodeExprBinary.Operator.GtEq, 2),
    Token.Type.SymbolPlus: (NodeExprBinary.Operator.Add, 3),
    Token.Type.SymbolMinus: (NodeExprBinary.Operator.Sub, 3),
    Token.Type.SymbolStar: (NodeExprBinary.Operator.Mul, 4),
    Token.Type.SymbolFSlash: (NodeExprBinary.Operator.Div, 4),
    Token.Type.SymbolPercent: (NodeExprBinary.Operator.Mod, 4),
}
UNARY_OPERATOR = {
    Token.Type.SymbolMinus: NodeExprUnary.Operator.Negative,
    Token.Type.SymbolBang: NodeExprUnary.Operator.Negate,
}
LITERALS = (
    Token.Type.Identifier,
    Token.Type.Integer,
    Token.Type.BooleanTrue, Token.Type.BooleanFalse,
)
BUILTIN_TYPES = (
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
STATEMENT_TYPES = (
    Token.Type.KeywordIf,
    Token.Type.KeywordWhile,
    Token.Type.KeywordDo,
    Token.Type.KeywordFor,
    Token.Type.SymbolLBrace,
    Token.Type.SymbolSemicolon,
)


## Functions
def _create_typed_node(token: Token) -> NodeTypeBuiltin:
    """Helper function for creating NodeTypeBuiltin by token"""
    _type: NodeTypeBuiltin.Type
    match token.type:
        case Token.Type.KeywordVoid:
            _type = NodeTypeBuiltin.Type.Void
        case Token.Type.KeywordBoolean:
            _type = NodeTypeBuiltin.Type.Boolean
        case Token.Type.KeywordInt8:
            _type = NodeTypeBuiltin.Type.Int8
        case Token.Type.KeywordInt16:
            _type = NodeTypeBuiltin.Type.Int16
        case Token.Type.KeywordInt32:
            _type = NodeTypeBuiltin.Type.Int32
        case Token.Type.KeywordInt64:
            _type = NodeTypeBuiltin.Type.Int64
        case Token.Type.KeywordUInt8:
            _type = NodeTypeBuiltin.Type.UInt8
        case Token.Type.KeywordUInt16:
            _type = NodeTypeBuiltin.Type.UInt16
        case Token.Type.KeywordUInt32:
            _type = NodeTypeBuiltin.Type.UInt32
        case Token.Type.KeywordUInt64:
            _type = NodeTypeBuiltin.Type.UInt64
        case _:
            raise TypeError(f"Unhandled token type ({token.type.name}) in create_typed_node")
    return NodeTypeBuiltin(token.location, _type)


def _create_literal_node(token: Token) -> NodeExprLiteral:
    """Helper function for creating NodeExprLiteral by token type and value"""
    match token.type:
        case Token.Type.Integer:
            value = int(token.value)
            return NodeExprLiteral.create_integer(token.location, value)
        case Token.Type.BooleanTrue:
            return NodeExprLiteral.create_boolean(token.location, True)
        case Token.Type.BooleanFalse:
            return NodeExprLiteral.create_boolean(token.location, False)
        case _:
            raise TypeError(f"Unhandled token type ({token.type.name}) in create_literal_node")


## Classes
class Parser(LookaheadBuffer[Token, Token.Type]):
    """
    Ember Language Parser
    Lookahead(n)

    Iterates over token stream and produces a given AST node
    where each grammar rule is represented as an internal method.
    """

    # -Constructor
    def __init__(self, tokens: Iterator[Token]):
        super().__init__(tokens, lambda token: token.type)
        self._last_token: Token

    # -Instance Methods
    def advance(self) -> Token | None:
        value = super().advance()
        if value:
            self._last_token = value
        return value

    def require(self, expected: Token.Type) -> None:
        '''Throws error if next token is not expected type'''
        if self.consume(expected):
            return
        token = self._last_token if self.is_at_end else self.peek()
        assert token is not None
        raise EmberParserError(token.location, f"Expected {expected.name} got {token.type.name}")

    def require_any(self, *expected: Token.Type) -> Token:
        '''Throws error if next token is not in expected types'''
        token = self.matches(*expected)
        if token is not None:
            _ = self.advance()
            return token
        token = self.peek()
        if token is None:
            raise EmberParserError(
                self._last_token.location,
                f"Unexpected end of token stream, expected one of {expected}"
            )
        raise EmberParserError(token.location, f"Unexpected token {token.type.name}; expected one of {expected}")

    def _sync(self) -> None:
        '''Sync the parser into the next correct state'''
        while token := self.advance():
            if token.type == Token.Type.SymbolSemicolon:
                break

    def parse(self) -> NodeDeclUnit:
        '''
        Grammar[Unit]
        declaration*;
        '''
        body: list[NodeBase] = []
        while not self.is_at_end:
            try:
                decl = self._parse_declaration()
                body.append(decl)
            except EmberParserError as e:
                print(e)
                self._sync()
        return NodeDeclUnit(body)

    def _parse_declaration(self) -> NodeBase:
        '''
        Grammar[Declaration]
        declaration_statement;
        '''
        return self._parse_declaration_statement()

    def _parse_declaration_statement(self) -> NodeBase:
        '''
        Grammar[Declaration:Statement]
        declaration_variable | statement;
        '''
        token = self.peek()
        # -Statement blocks
        if token is not None and token.type in STATEMENT_TYPES:
            return self._parse_statement()
        # -Type declarations
        is_decl, node = self._try_parse_type_decl()
        if is_decl:
            return self._parse_declaration_variable(node)
        # -Statement Expression
        node = cast(NodeExpr, node)
        return self._parse_statement(node)

    def _parse_type(self) -> NODE_TYPE:
        '''Returns a parsed type node'''
        return cast(NODE_TYPE, self._parse_expression_unary())

    def _try_parse_type_decl(self) -> tuple[bool, NODE_TYPE]:
        '''Try to parse a type token and return if type declaration'''
        _type = self._parse_type()
        token = self.peek()
        is_type = True if token is not None and token.type == Token.Type.Identifier else False
        return (is_type, _type)

    def _parse_declaration_variable(
        self, type_node: NODE_TYPE | None = None
    ) -> NodeDeclVariable:
        '''
        Grammar[Declaration:Variable]
        TYPE IDENTIFIER ('=' expression)? ';';
        '''
        assert type_node is not None
        self.require(Token.Type.Identifier)
        ident = self._last_token
        initializer: NodeExpr | None = None
        if self.consume(Token.Type.SymbolEq):
            initializer = cast(NodeExpr, self._parse_expression())
        self.require(Token.Type.SymbolSemicolon)
        return NodeDeclVariable(ident.location, type_node, ident.value, initializer)

    def _parse_statement(self, node: NodeExpr | None = None) -> NodeBase:
        '''
        Grammar[Statement]
        statement_block | statement_condition | statement_expression | ';';
        '''
        if node is None:
            # -Block statement
            if self.consume(Token.Type.SymbolLBrace):
                return self._parse_statement_block()
            # -Conditional statement
            elif self.consume(Token.Type.KeywordIf):
                return self._parse_statement_conditional()
            # -Loop:While statement
            elif self.consume(Token.Type.KeywordWhile):
                return self._parse_statement_loop_while()
            # -Loop:Do statement
            elif self.consume(Token.Type.KeywordDo):
                return self._parse_statement_loop_do()
            # -Loop:For statement
            elif self.consume(Token.Type.KeywordFor):
                return self._parse_statement_loop_for()
            # -Empty statement
            elif self.consume(Token.Type.SymbolSemicolon):
                return NodeStmtExpression(self._last_token.location, None)
            return self._parse_statement_expression()
        expr = cast(NodeExpr, self._parse_expression(node))
        return self._parse_statement_expression(expr)

    def _parse_statement_block(self) -> NodeBase:
        '''
        Grammar[Statement:Block]
        '{' declaration_statement* '}';
        '''
        token = self._last_token
        body: list[NodeBase] = []
        while not self.consume(Token.Type.SymbolRBrace):
            stmt = self._parse_declaration_statement()
            body.append(stmt)
        return NodeStmtBlock(token.location, body)

    def _parse_statement_conditional(self) -> NodeBase:
        '''
        Grammar[Statement:Conditional]
        if '(' expression ')' statement ('else' statement)?;
        '''
        token = self._last_token
        self.require(Token.Type.SymbolLParen)
        condition = cast(NodeExpr, self._parse_expression())
        self.require(Token.Type.SymbolRParen)
        body = cast(NodeStmt, self._parse_statement())
        else_body: NodeStmt | None = None
        if self.consume(Token.Type.KeywordElse):
            else_body = cast(NodeStmt, self._parse_statement())
        return NodeStmtConditional(token.location, condition, body, else_body)

    def _parse_statement_loop_while(self) -> NodeStmtLoop:
        '''
        Grammar[Statement:Loop:While]
        'while' '(' expression ')' statement;
        '''
        token = self._last_token
        self.require(Token.Type.SymbolLParen)
        condition = cast(NodeExpr, self._parse_expression())
        self.require(Token.Type.SymbolRParen)
        body = cast(NodeStmt, self._parse_statement())
        return NodeStmtLoop(token.location, condition, body)

    def _parse_statement_loop_do(self) -> NodeStmtBlock:
        '''
        Grammar[Statement:Loop:Do]
        'do' statement 'while' '(' expression ')' ';';
        '''
        do_token = self._last_token
        body = cast(NodeStmt, self._parse_statement())
        self.require(Token.Type.KeywordWhile)
        while_token = self._last_token
        self.require(Token.Type.SymbolLParen)
        condition = cast(NodeExpr, self._parse_expression())
        self.require(Token.Type.SymbolRParen)
        self.require(Token.Type.SymbolSemicolon)
        loop = NodeStmtLoop(while_token.location, condition, body)
        return NodeStmtBlock(do_token.location, [body, loop])

    def _parse_statement_loop_for(self) -> NodeStmt:
        '''
        Grammar[Statement:Loop:For]
        'for' '(' (declaration_variable | statement_expression | ';') expression? ';' expression? ')' statement;
        '''
        self.require(Token.Type.SymbolLParen)
        # -<Initializer>-
        init: NodeBase | None = None
        if not self.consume(Token.Type.SymbolSemicolon):
            is_decl, node = self._try_parse_type_decl()
            if is_decl:
                init = self._parse_declaration_variable(node)
            else:
                node = cast(NodeExpr, node)
                init = self._parse_expression(node)
                self.require(Token.Type.SymbolSemicolon)
        # -<Condition>-
        condition: NodeExpr
        if not self.consume(Token.Type.SymbolSemicolon):
            condition = cast(NodeExpr, self._parse_expression())
            self.require(Token.Type.SymbolSemicolon)
        else:
            token = self._last_token
            condition = NodeExprLiteral.create_boolean(token.location, True)
        # -<Increment>-
        inc: NodeStmt | None = None
        if not self.consume(Token.Type.SymbolRParen):
            inc_expr = cast(NodeExpr, self._parse_expression())
            self.require(Token.Type.SymbolRParen)
            inc = NodeStmtExpression(self._last_token.location, inc_expr)
        # -<Body>-
        body = cast(NodeStmt, self._parse_statement())
        if inc is not None:
            body = NodeStmtBlock(body.location, [body, inc])
        loop = NodeStmtLoop(condition.location, condition, body)
        if init is None:
            return loop
        return NodeStmtBlock(init.location, [init, loop])

    def _parse_statement_expression(
        self, expr: NodeExpr | None = None
    ) -> NodeStmtExpression:
        '''
        Grammar[Statement:Expression]
        expression ';';
        '''
        if expr is None:
            expr = cast(NodeExpr, self._parse_expression())
        self.require(Token.Type.SymbolSemicolon)
        return NodeStmtExpression(expr.location, expr)

    def _parse_expression(self, l_value: NodeExpr | None = None) -> NodeBase:
        '''
        Grammar[Expression]
        expression_binary ('=' expression)?;
        '''
        l_value = cast(NodeExpr, self._parse_expression_binary(lhs=l_value))
        if self.consume(Token.Type.SymbolEq):
            location = self._last_token.location
            r_value = cast(NodeExpr, self._parse_expression())
            l_value = NodeExprAssignment(location, l_value, r_value)
        return l_value

    def _parse_expression_binary(
        self, current: int = 0, lhs: NodeExpr | None = None
    ) -> NodeBase:
        '''
        Grammar[Expression:Binary]
        expression_unary (BINARY_OPERATOR expression_binary)*;
        '''
        if lhs is None:
            lhs = cast(NodeExpr, self._parse_expression_unary())
        while token := self.matches(*BINARY_OPERATOR.keys()):
            operator, precedence = BINARY_OPERATOR[token.type]
            if precedence <= current:
                break
            _ = self.advance()
            rhs = cast(NodeExpr, self._parse_expression_binary(precedence))
            lhs = NodeExprBinary(token.location, operator, lhs, rhs)
        return lhs

    def _parse_expression_unary(self) -> NodeBase:
        '''
        Grammar[Expression:Unary]
        UNARY_OPERATOR expression_unary | expression_primary;
        '''
        if token := self.matches(*UNARY_OPERATOR.keys()):
            operator = UNARY_OPERATOR[token.type]
            _ = self.advance()
            expression = cast(NodeExpr, self._parse_expression_unary())
            return NodeExprUnary(token.location, operator, expression)
        return self._parse_expression_primary()

    def _parse_expression_primary(self) -> NodeBase:
        '''
        Grammar[Expression:Primary]
        '(' expression ')' | expression_literal;
        '''
        if not self.consume(Token.Type.SymbolLParen):
            return self._parse_expression_literal()
        location = self._last_token.location
        expression = cast(NodeExpr, self._parse_expression())
        self.require(Token.Type.SymbolRParen)
        return NodeExprGroup(location, expression)

    def _parse_expression_literal(self) -> NODE_TYPE:
        '''
        Grammar[Expression:Literal]
        TYPE | IDENTIFIER | BOOLEAN | INTEGER;
        '''
        if token := self.matches(*BUILTIN_TYPES):
            self.advance()
            return _create_typed_node(token)
        elif self.consume(Token.Type.Identifier):
            token = self._last_token
            return NodeExprVariable(token.location, token.value)
        token = self.require_any(*LITERALS)
        return _create_literal_node(token)

    # -Properties
    @property
    def is_at_end(self) -> bool:
        return self.peek() is None
