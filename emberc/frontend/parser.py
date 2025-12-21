##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Parser              ##
##-------------------------------##

## Imports
from collections.abc import Iterator
from .lookahead_buffer import LookaheadBuffer
from .token import Token
from ..middleware.nodes import (
    LITERAL, NodeBase, NodeDecl, NodeStmt, NodeExpr,
    NodeDeclUnit,
    NodeStmtExpression,
    NodeExprGroup, NodeExprBinary, NodeExprUnary,
    NodeExprLiteral,
)

## Constants
BINARY_OPERATOR = {
    # -Math
    Token.Type.SymbolPlus: (NodeExprBinary.Operator.Add, 1),
    Token.Type.SymbolMinus: (NodeExprBinary.Operator.Sub, 1),
    Token.Type.SymbolStar: (NodeExprBinary.Operator.Mul, 2),
    Token.Type.SymbolFSlash: (NodeExprBinary.Operator.Div, 2),
    Token.Type.SymbolPercent: (NodeExprBinary.Operator.Mod, 2),
}
UNARY_OPERATOR = {
    Token.Type.SymbolMinus: NodeExprUnary.Operator.Negative,
}


## Functions
def _create_literal_node(token: Token) -> NodeExprLiteral:
    """Helper function for creating NodeExprLiteral by token type and value"""
    match token.type:
        case Token.Type.Integer:
            value = int(token.value)
            return NodeExprLiteral.create_integer(token.location, value)
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

    def parse(self) -> NodeDeclUnit:
        '''
        Grammar[Unit]
        statement;
        '''
        statements: list[NodeStmt] = []
        while not self.is_at_end:
            stmt = self._parse_statement()
            statements.append(stmt)
        return NodeDeclUnit(statements)

    def _parse_statement(self) -> NodeStmt:
        '''
        Grammar[Statement]
        expression? ';';
        '''
        if self.consume(Token.Type.SymbolSemicolon):
            return NodeStmtExpression(self._last_token.location, None)
        expr = self._parse_expression()
        if not self.consume(Token.Type.SymbolSemicolon):
            pass  # TODO: Error handling
        return NodeStmtExpression(expr.location, expr)

    def _parse_expression(self) -> NodeExpr:
        '''
        Grammar[Expression]
        expression_binary;
        '''
        return self._parse_expression_binary()

    def _parse_expression_binary(self, current: int = 0) -> NodeExpr:
        '''
        Grammar[Expression:Binary]
        expression_primary (BINARY_OPERATOR expression_binary)*;
        '''
        lhs = self._parse_expression_unary()
        while token := self.matches(*BINARY_OPERATOR.keys()):
            operator, precedence = BINARY_OPERATOR[token.type]
            if precedence <= current:
                break
            _ = self.advance()
            rhs = self._parse_expression_binary(precedence)
            lhs = NodeExprBinary(token.location, operator, lhs, rhs)
        return lhs

    def _parse_expression_unary(self) -> NodeExpr:
        '''
        Grammar[Expression:Unary]
        UNARY_OPERATOR expression_unary | expression_primary;
        '''
        if token := self.matches(*UNARY_OPERATOR.keys()):
            operator = UNARY_OPERATOR[token.type]
            _ = self.advance()
            expression = self._parse_expression_unary()
            return NodeExprUnary(token.location, operator, expression)
        return self._parse_expression_primary()

    def _parse_expression_primary(self) -> NodeExpr:
        '''
        Grammar[Expression:Primary]
        '(' expression ')' | expression_literal;
        '''
        if not self.consume(Token.Type.SymbolLParen):
            return self._parse_expression_literal()
        location = self._last_token.location
        expression = self._parse_expression()
        if not self.consume(Token.Type.SymbolRParen):
            pass  # TODO: Error handling
        return NodeExprGroup(location, expression)

    def _parse_expression_literal(self) -> NodeExprLiteral:
        '''
        Grammar[Expression:Literal]
        NUMBER;
        '''
        token = self.advance()
        assert token is not None  # TODO: Error handling
        return _create_literal_node(token)

    # -Properties
    @property
    def is_at_end(self) -> bool:
        return self.peek() is None
