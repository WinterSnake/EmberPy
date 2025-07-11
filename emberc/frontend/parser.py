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
    Node, NodeExpr, NodeModule,
    NodeStmtDeclVar, NodeStmtBlock, NodeStmtExpr,
    NodeExprBinary, NodeExprUnary, NodeExprGroup,
    NodeExprAssign, NodeExprId, NodeExprLiteral,
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
VARIABLE_TYPES: tuple[Token.Type, ...] = (
    # -Ints
    Token.Type.Int8,
    Token.Type.Int16,
    Token.Type.Int32,
    Token.Type.Int64,
    # -UInts
    Token.Type.UInt8,
    Token.Type.UInt16,
    Token.Type.UInt32,
    Token.Type.UInt64,
)


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
        '''
        Grammar[Module]
        statement*;
        '''
        statements: list[Node] = []
        while not self.is_at_end:
            if self._peek() is None:
                break
            node = self._parse_statement()
            statements.append(node)
        return NodeModule(statements)

    def _parse_statement(self) -> Node:
        '''
        Grammar[Statement]
        statement_block |
        ( (statement_declaration_variable | statement_expression) ';');
        '''
        node: Node
        if (self._consume(Token.Type.LBrace)):
            node = self._parse_statement_block()
        elif (token := self._match(*VARIABLE_TYPES)):
            node = self._parse_statement_declaration_variable(token)
        else:
            node = self._parse_statement_expression()
        # -TODO: Error Handling
        if not self._consume(Token.Type.Semicolon):
            pass
        return node

    def _parse_statement_block(self) -> Node:
        '''
        Grammar[Statement::Declartion::Block]
        '{' statement* '}';
        '''
        statements: list[Node] = []
        while not self._consume(Token.Type.RBrace):
            # -TODO: Error Handling
            if self._peek() is None:
                break
            node = self._parse_statement()
            statements.append(node)
        return NodeStmtBlock(statements)

    def _parse_statement_declaration_variable(self, token: Token) -> Node:
        '''
        Grammar[Statement::Declartion::Variable]
        TYPE IDENTIFIER ('=' expression)?;
        '''
        _id = self._next()
        # -TODO: Error Handling
        assert _id is not None
        assert _id.type == Token.Type.Identifier
        assert _id.value is not None
        init: NodeExpr | None = None
        if self._consume(Token.Type.Eq):
            init = self._parse_expression()
        return NodeStmtDeclVar(_id.value, init)

    def _parse_statement_expression(self) -> Node:
        '''
        Grammar[Statement::Expression]
        expression;
        '''
        return NodeStmtExpr(self._parse_expression())

    def _parse_expression(self) -> NodeExpr:
        '''
        Grammar[Expression]
        expression_assignment;
        '''
        return self._parse_expression_assignment()

    def _parse_expression_assignment(self) -> NodeExpr:
        '''
        Grammar[Expression::Assignment]
        (IDENTIFIER '=' expression_assignment) | expression_binary;
        '''
        node: NodeExpr = self._parse_expression_binary()
        if self._consume(Token.Type.Eq):
            location = self._last_token.location
            # -TODO: Error Handling
            assert isinstance(node, NodeExprId)
            r_value = self._parse_expression_assignment()
            node = NodeExprAssign(location, node, r_value)
        return node

    def _parse_expression_binary(self) -> NodeExpr:
        '''
        Grammar[Expression::Binary]
        expression_binary_term;
        '''
        return self._parse_expression_binary_term()

    def _parse_expression_binary_term(self) -> NodeExpr:
        '''
        Grammar[Expression::Binary::Term]
        expression_binary_factor ( ('+' | '-') expression_binary_factor)*;
        '''
        node = self._parse_expression_binary_factor()
        while (token := self._match(Token.Type.Plus, Token.Type.Minus)):
            operator = OPERATOR_BINARY[token.type]
            rhs = self._parse_expression_binary_factor()
            node = NodeExprBinary(token.location, operator, node, rhs)
        return node

    def _parse_expression_binary_factor(self) -> NodeExpr:
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

    def _parse_expression_unary(self) -> NodeExpr:
        '''
        Grammar[Expression::Unary]
        ('-' unary) | primary;
        '''
        if (token := self._match(Token.Type.Minus)):
            operator = OPERATOR_UNARY[token.type]
            node = self._parse_expression_unary()
            return NodeExprUnary(token.location, operator, node)
        return self._parse_primary()

    def _parse_primary(self) -> NodeExpr:
        '''
        Grammar[Expression::Primary]
        IDENTIFIER | expression_literal | '(' expression ')';
        '''
        if self._consume(Token.Type.LParen):
            location = self._last_token.location
            node = self._parse_expression()
            # -TODO: Error Handling
            if not self._consume(Token.Type.RParen):
                pass
            return NodeExprGroup(location, node)
        elif (token := self._match(Token.Type.Identifier)):
            assert token.value is not None
            return NodeExprId(token.location, token.value)
        return self._parse_literal()

    def _parse_literal(self) -> NodeExpr:
        '''
        Grammar[Expression::Literal]
        NUMBER;
        '''
        token = self._next()
        # -TODO: Error Handling
        assert token is not None
        assert token.value is not None
        assert token.type is Token.Type.Integer
        return NodeExprLiteral(
            token.location, NodeExprLiteral.Type.Integer, int(token.value)
        )
