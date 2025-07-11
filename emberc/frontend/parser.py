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
    NodeStmtIf, NodeStmtLoop,
    NodeExprBinary, NodeExprUnary, NodeExprGroup,
    NodeExprAssign, NodeExprId, NodeExprLiteral,
)

## Constants
OPERATOR_BINARY: dict[Token.Type, NodeExprBinary.Type] = {
    Token.Type.SymbolPlus: NodeExprBinary.Type.Add,
    Token.Type.SymbolMinus: NodeExprBinary.Type.Sub,
    Token.Type.SymbolStar: NodeExprBinary.Type.Mul,
    Token.Type.SymbolFSlash: NodeExprBinary.Type.Div,
    Token.Type.SymbolPercent: NodeExprBinary.Type.Mod,
    Token.Type.SymbolLt: NodeExprBinary.Type.Lt,
    Token.Type.SymbolGt: NodeExprBinary.Type.Gt,
    Token.Type.SymbolLtEq: NodeExprBinary.Type.LtEq,
    Token.Type.SymbolGtEq: NodeExprBinary.Type.GtEq,
    Token.Type.SymbolEqEq: NodeExprBinary.Type.EqEq,
    Token.Type.SymbolBangEq: NodeExprBinary.Type.NtEq,
}
OPERATOR_UNARY: dict[Token.Type, NodeExprUnary.Type] = {
    Token.Type.SymbolBang: NodeExprUnary.Type.Negate,
    Token.Type.SymbolMinus: NodeExprUnary.Type.Negative,
}
VARIABLE_TYPES: tuple[Token.Type, ...] = (
    Token.Type.KeywordBoolean,
    # -Ints
    Token.Type.KeywordInt8,
    Token.Type.KeywordInt16,
    Token.Type.KeywordInt32,
    Token.Type.KeywordInt64,
    # -UInts
    Token.Type.KeywordUInt8,
    Token.Type.KeywordUInt16,
    Token.Type.KeywordUInt32,
    Token.Type.KeywordUInt64,
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
        declaration*;
        '''
        body: list[Node] = []
        while not self.is_at_end:
            if self._peek() is None:
                break
            node = self._parse_declaration()
            body.append(node)
        return NodeModule(body)

    def _parse_declaration(self) -> Node:
        '''
        Grammar[Declaration]
        declaration_variable | statement;
        '''
        print(f"[Parser::Decl]")
        if (token := self._match(*VARIABLE_TYPES)):
            return self._parse_declaration_variable(token)
        return self._parse_statement()

    def _parse_declaration_variable(self, token: Token) -> Node:
        '''
        Grammar[Declaration::Variable]
        TYPE IDENTIFIER ('=' expression)? ';';
        '''
        print(f"[Parser::Decl::Var]")
        _id = self._next()
        # -TODO: Error Handling
        assert _id is not None
        assert _id.type == Token.Type.Identifier
        assert _id.value is not None
        init: NodeExpr | None = None
        if self._consume(Token.Type.SymbolEq):
            init = self._parse_expression()
        # -TODO: Error Handling
        assert self._consume(Token.Type.SymbolSemicolon)
        return NodeStmtDeclVar(_id.value, init)

    def _parse_statement(self) -> Node:
        '''
        Grammar[Statement]
        statement_if | statement_while | statement_block | statment_expression;
        '''
        print(f"[Parser::Stmt]")
        # -Rule: If
        if self._consume(Token.Type.KeywordIf):
            return self._parse_statement_if()
        # -Rule: While
        if self._consume(Token.Type.KeywordWhile):
            return self._parse_statement_while()
        # -Rule: Block
        elif self._consume(Token.Type.SymbolLBrace):
            return self._parse_statement_block()
        # -Rule: Expression
        return self._parse_statement_expression()

    def _parse_statement_if(self) -> Node:
        '''
        Grammar[Statement::If]
        'if' '(' expression ')' statement ('else' statement)?;
        '''
        print(f"[Parser::Stmt::If]")
        # -TODO: Error Handling
        assert self._consume(Token.Type.SymbolLParen)
        condition = self._parse_expression()
        # -TODO: Error Handling
        assert self._consume(Token.Type.SymbolRParen)
        body = self._parse_statement()
        branch: Node | None = None
        if self._consume(Token.Type.KeywordElse):
            branch = self._parse_statement()
        return NodeStmtIf(condition, body, branch)

    def _parse_statement_while(self) -> Node:
        '''
        Grammar[Statement::While]
        'while' '(' expression ')' statement;
        '''
        print(f"[Parser::Stmt::While]")
        # -TODO: Error Handling
        assert self._consume(Token.Type.SymbolLParen)
        condition = self._parse_expression()
        # -TODO: Error Handling
        assert self._consume(Token.Type.SymbolRParen)
        body = self._parse_statement()
        return NodeStmtLoop(condition, body)

    def _parse_statement_block(self) -> Node:
        '''
        Grammar[Statement::Block]
        '{' declaration* '}';
        '''
        print(f"[Parser::Stmt::Block]")
        body: list[Node] = []
        while not self._consume(Token.Type.SymbolRBrace):
            # -TODO: Error Handling
            assert not self.is_at_end
            node = self._parse_declaration()
            body.append(node)
        return NodeStmtBlock(body)

    def _parse_statement_expression(self) -> Node:
        '''
        Grammar[Statement::Expression]
        expression ';';
        '''
        print(f"[Parser::Stmt::Expr]")
        node = self._parse_expression()
        # -TODO: Error Handling
        assert self._consume(Token.Type.SymbolSemicolon)
        return NodeStmtExpr(node)

    def _parse_expression(self) -> NodeExpr:
        '''
        Grammar[Expression]
        expression_assignment;
        '''
        print(f"[Parser::Expr]")
        return self._parse_expression_assignment()

    def _parse_expression_assignment(self) -> NodeExpr:
        '''
        Grammar[Expression::Assignment]
        IDENTIFIER '=' expression_assignment | expression_binary;
        '''
        print(f"[Parser::Expr::Assign]")
        node = self._parse_expression_binary()
        if self._consume(Token.Type.SymbolEq):
            location = self._last_token.location
            # -TODO: Error Handling
            assert isinstance(node, NodeExprId)
            r_value = self._parse_expression_assignment()
            node = NodeExprAssign(location, node, r_value)
        return node

    def _parse_expression_binary(self) -> NodeExpr:
        '''
        Grammar[Expression::Binary]
        expression_unary ( ('+', '-', '*', '/', '%', '<', '>', '>=', '<=', '==', '!=') expression_unary)*;
        '''
        print(f"[Parser::Expr::Binary]")
        # -Internal Functions
        def _equality() -> NodeExpr:
            '''Handle "==" and "!=" tokens'''
            print(f"[Parser::Expr::Binary::Equality]")
            node = _comparison()
            while (token := self._match(Token.Type.SymbolEqEq, Token.Type.SymbolBangEq)):
                operator = OPERATOR_BINARY[token.type]
                rhs = _comparison()
                node = NodeExprBinary(token.location, operator, node, rhs)
            return node

        def _comparison() -> NodeExpr:
            '''Handle "<", ">", "<=" and ">=" tokens'''
            print(f"[Parser::Expr::Binary::Comparison]")
            node = _term()
            while (token := self._match(
                Token.Type.SymbolLt, Token.Type.SymbolGt,
                Token.Type.SymbolLtEq, Token.Type.SymbolGtEq
            )):
                operator = OPERATOR_BINARY[token.type]
                rhs = _term()
                node = NodeExprBinary(token.location, operator, node, rhs)
            return node

        def _term() -> NodeExpr:
            '''Handle "+" and "-" tokens'''
            print(f"[Parser::Expr::Binary::Term]")
            node = _factor()
            while (token := self._match(Token.Type.SymbolPlus, Token.Type.SymbolMinus)):
                operator = OPERATOR_BINARY[token.type]
                rhs = _factor()
                node = NodeExprBinary(token.location, operator, node, rhs)
            return node

        def _factor() -> NodeExpr:
            '''Handle "*", "/", and "%" tokens'''
            print(f"[Parser::Expr::Binary::Factor]")
            node = self._parse_expression_unary()
            while (token := self._match(
                Token.Type.SymbolStar, Token.Type.SymbolFSlash, Token.Type.SymbolPercent
            )):
                operator = OPERATOR_BINARY[token.type]
                rhs = self._parse_expression_unary()
                node = NodeExprBinary(token.location, operator, node, rhs)
            return node

        # -Body
        return _equality()

    def _parse_expression_unary(self) -> NodeExpr:
        '''
        Grammar[Expression::Unary]
        ('-' | '!') expression_unary | expression_primary;
        '''
        print(f"[Parser::Expr::Unary]")
        if (token := self._match(*OPERATOR_UNARY.keys())):
            operator = OPERATOR_UNARY[token.type]
            node = self._parse_expression_unary()
            return NodeExprUnary(token.location, operator, node)
        return self._parse_expression_primary()

    def _parse_expression_primary(self) -> NodeExpr:
        '''
        Grammar[Expression::Primary]
        IDENTIFIER | expression_literal | '(' expression ')';
        '''
        print(f"[Parser::Expr::Primary]")
        # -Rule: Identifier
        if (token := self._match(Token.Type.Identifier)):
            assert token.value is not None
            return NodeExprId(token.location, token.value)
        # -Rule: Group
        if self._consume(Token.Type.SymbolLParen):
            location = self._last_token.location
            node = self._parse_expression()
            # -TODO: Error Handling
            assert self._consume(Token.Type.SymbolRParen)
            return NodeExprGroup(location, node)
        # -Rule: Literal
        return self._parse_expression_literal()

    def _parse_expression_literal(self) -> NodeExpr:
        '''
        Grammar[Expression::Literal]
        BOOLEAN | NUMBER;
        '''
        print(f"[Parser::Expr::Literal]")
        token = self._next()
        # -TODO: Error Handling
        assert token is not None
        _type: NodeExprLiteral.Type
        value: bool | int
        match token.type:
            case Token.Type.LiteralTrue:
                _type = NodeExprLiteral.Type.Boolean
                value = True
            case Token.Type.LiteralFalse:
                _type = NodeExprLiteral.Type.Boolean
                value = False
            case Token.Type.Integer:
                _type = NodeExprLiteral.Type.Integer
                assert token.value is not None
                value = int(token.value)
            case _:
                assert False
        return NodeExprLiteral(token.location, _type, value)
