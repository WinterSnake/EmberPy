##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Parser                        ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Iterator
from typing import cast
from .token import Token
from ..middleware.nodes import (
    Node, NodeExpr, NodeModule,
    NodeStmtBlock, NodeStmtConditional, NodeStmtLoop,
    NodeDeclFunction, NodeDeclVariable, NodeStmtExpression,
    NodeStmtReturn, NodeExprAssignment, NodeExprCall,
    NodeExprBinary, NodeExprUnary,
    NodeExprGroup, NodeExprVariable, NodeExprLiteral,
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
    Token.Type.KeywordVoid,
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
    def __init__(self, token_iter: Iterator[Token], debug_mode: bool = False) -> None:
        self.debug_mode: bool = debug_mode
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

    def _match(self, *types: Token.Type) -> bool:
        '''Returns next token if token matches expected type'''
        token = self._peek()
        if token is None or token.type not in types:
            return False
        self._lookahead = None
        return True

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
        declaration_function | declaration_variable | statement;
        '''
        if self.debug_mode:
            print(f"[Parser::Decl]")
        # -Rule: Declaration Function
        if self._consume(Token.Type.KeywordFunction):
            return self._parse_declaration_function()
        # -Rule: Declaration Variable
        if self._match(*VARIABLE_TYPES):
            return self._parse_declaration_variable()
        # -Rule: Statement
        return self._parse_statement()

    def _parse_declaration_function(self) -> Node:
        '''
        Grammar[Declaration::Function]
        'fn' IDENTIFIER '(' (TYPE IDENTIFIER (',' TYPE IDENTIFIER)*)? ')' ':' TYPE statement;
        '''
        if self.debug_mode:
            print(f"[Parser::Decl::Function]")
        # -Internal Functions
        def _parameter() -> str:
            '''
            TYPE IDENTIFIER
            '''
            if self.debug_mode:
                print(f"[Parser::Decl::Function::Parameter]")
            # -TODO: Error Handling
            assert self._match(*VARIABLE_TYPES)
            _type = self._last_token
            _id = self._next()
            # -TODO: Error Handling
            assert _id is not None
            assert _id.type == Token.Type.Identifier
            assert _id.value is not None
            return _id.value

        # -Body
        location = self._last_token.location
        _id = self._next()
        # -TODO: Error Handling
        assert _id is not None
        assert _id.type == Token.Type.Identifier
        assert _id.value is not None
        # -TODO: Error Handling
        assert self._consume(Token.Type.SymbolLParen)
        parameters: list[str] | None = None
        # -Parameters: 0
        if not self._consume(Token.Type.SymbolRParen):
            # -Parameters: 1
            parameters = [_parameter()]
            # -Parameters: 2+
            while self._consume(Token.Type.SymbolComma):
                parameters.append(_parameter())
            # -TODO: Error Handling
            assert self._consume(Token.Type.SymbolRParen)
        # -TODO: Error Handling
        assert self._consume(Token.Type.SymbolColon)
        # -TODO: Error Handling
        assert self._match(*VARIABLE_TYPES)
        _type = self._last_token
        # -TODO: Error Handling
        body = self._parse_statement()
        return NodeDeclFunction(_id.value, parameters, body)

    def _parse_declaration_variable(self) -> Node:
        '''
        Grammar[Declaration::Variable]
        TYPE IDENTIFIER ('=' expression)? ';';
        '''
        if self.debug_mode:
            print(f"[Parser::Decl::Var]")
        _type = self._last_token
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
        return NodeDeclVariable(_id.value, init)

    def _parse_statement(self) -> Node:
        '''
        Grammar[Statement]
        statement_if | statement_while | statement_for | statement_do |
        statement_block | statement_return | statment_expression;
        '''
        if self.debug_mode:
            print(f"[Parser::Stmt]")
        rule_table: dict[Token.Type, Callable[[], Node]] = {
            Token.Type.KeywordIf: self._parse_statement_if,
            Token.Type.KeywordWhile: self._parse_statement_while,
            Token.Type.KeywordDo: self._parse_statement_do,
            Token.Type.KeywordFor: self._parse_statement_for,
            Token.Type.KeywordReturn: self._parse_statement_return,
            Token.Type.SymbolLBrace: self._parse_statement_block,
        }
        # -Rule: Table Lookup
        if self._match(*rule_table.keys()):
            token = self._last_token
            return rule_table[token.type]()
        # -Rule: Expression
        return self._parse_statement_expression()

    def _parse_statement_if(self) -> Node:
        '''
        Grammar[Statement::If]
        'if' '(' expression ')' statement ('else' statement)?;
        '''
        if self.debug_mode:
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
        return NodeStmtConditional(condition, body, branch)

    def _parse_statement_while(self) -> Node:
        '''
        Grammar[Statement::While]
        'while' '(' expression ')' statement;
        '''
        if self.debug_mode:
            print(f"[Parser::Stmt::While]")
        # -TODO: Error Handling
        assert self._consume(Token.Type.SymbolLParen)
        condition = self._parse_expression()
        # -TODO: Error Handling
        assert self._consume(Token.Type.SymbolRParen)
        body = self._parse_statement()
        return NodeStmtLoop(condition, body)

    def _parse_statement_do(self) -> Node:
        '''
        Grammar[Statement::Do]
        'do' '{' declaration* '}' 'while' '(' expression ')' ';';
        '''
        if self.debug_mode:
            print(f"[Parser::Stmt::Do]")
        # -TODO: Error Handling
        assert self._consume(Token.Type.SymbolLBrace)
        body = self._parse_statement_block()
        # -TODO: Error Handling
        assert self._consume(Token.Type.KeywordWhile)
        assert self._consume(Token.Type.SymbolLParen)
        condition = self._parse_expression()
        # -TODO: Error Handling
        assert self._consume(Token.Type.SymbolRParen)
        assert self._consume(Token.Type.SymbolSemicolon)
        loop = NodeStmtLoop(condition, body)
        return NodeStmtBlock([body, loop])

    def _parse_statement_for(self) -> Node:
        '''
        Grammar[Statement::For]
        'for' '(' (declaration_variable | statement_expression | ';') expression? ';' expression? ')' statement;
        '''
        if self.debug_mode:
            print(f"[Parser::Stmt::For]")
        # -TODO: Error Handling
        assert self._consume(Token.Type.SymbolLParen)
        # -Initializer
        initializer: Node | None = None
        if not self._consume(Token.Type.SymbolSemicolon):
            if self._match(*VARIABLE_TYPES):
                initializer = self._parse_declaration_variable()
            else:
                initializer = self._parse_statement_expression()
        # -Condition
        condition: NodeExpr | None = None
        if not self._consume(Token.Type.SymbolSemicolon):
            condition = self._parse_expression()
            # -TODO: Error Handling
            assert self._consume(Token.Type.SymbolSemicolon)
        condition_location = self._last_token.location
        # -Increment
        increment: NodeExpr | None = None
        if not self._consume(Token.Type.SymbolRParen):
            increment = self._parse_expression()
            # -TODO: Error Handling
            assert self._consume(Token.Type.SymbolRParen)
        body = self._parse_statement()
        # -Desugar
        if increment is not None:
            body = NodeStmtBlock([body, increment])
        if condition is None:
            condition = NodeExprLiteral(
                condition_location, NodeExprLiteral.Type.Boolean, True
            )
        body = NodeStmtLoop(condition, body)
        if initializer is not None:
            body = NodeStmtBlock([initializer, body])
        return body


    def _parse_statement_block(self) -> Node:
        '''
        Grammar[Statement::Block]
        '{' declaration* '}';
        '''
        if self.debug_mode:
            print(f"[Parser::Stmt::Block]")
        body: list[Node] = []
        while not self._consume(Token.Type.SymbolRBrace):
            # -TODO: Error Handling
            assert not self.is_at_end
            node = self._parse_declaration()
            body.append(node)
        return NodeStmtBlock(body)

    def _parse_statement_return(self) -> Node:
        '''
        Grammar[Statement::Return]
        'return' expression? ';';
        '''
        location = self._last_token.location
        value: NodeExpr | None = None
        if not self._consume(Token.Type.SymbolSemicolon):
            value = self._parse_expression()
            # -TODO: Error Handling
            assert self._consume(Token.Type.SymbolSemicolon)
        return NodeStmtReturn(value)

    def _parse_statement_expression(self) -> Node:
        '''
        Grammar[Statement::Expression]
        expression ';';
        '''
        if self.debug_mode:
            print(f"[Parser::Stmt::Expr]")
        node = self._parse_expression()
        # -TODO: Error Handling
        assert self._consume(Token.Type.SymbolSemicolon)
        return NodeStmtExpression(node)

    def _parse_expression(self) -> NodeExpr:
        '''
        Grammar[Expression]
        expression_assignment;
        '''
        if self.debug_mode:
            print(f"[Parser::Expr]")
        return self._parse_expression_assignment()

    def _parse_expression_assignment(self) -> NodeExpr:
        '''
        Grammar[Expression::Assignment]
        IDENTIFIER '=' expression_assignment | expression_binary;
        '''
        if self.debug_mode:
            print(f"[Parser::Expr::Assign]")
        node = self._parse_expression_binary()
        if self._consume(Token.Type.SymbolEq):
            location = self._last_token.location
            # -TODO: Error Handling
            assert isinstance(node, NodeExprVariable)
            r_value = self._parse_expression_assignment()
            node = NodeExprAssignment(location, node.id, r_value)
        return node

    def _parse_expression_binary(self) -> NodeExpr:
        '''
        Grammar[Expression::Binary]
        expression_unary_prefix ( ('+', '-', '*', '/', '%', '<', '>', '>=', '<=', '==', '!=') expression_unary_prefix)*;
        '''
        if self.debug_mode:
            print(f"[Parser::Expr::Binary]")
        # -Internal Functions
        def _equality() -> NodeExpr:
            '''
            comparison ( ("==" | "!=") comparison)*;
            '''
            if self.debug_mode:
                print(f"[Parser::Expr::Binary::Equality]")
            node = _comparison()
            while self._match(Token.Type.SymbolEqEq, Token.Type.SymbolBangEq):
                token = self._last_token
                operator = OPERATOR_BINARY[token.type]
                rhs = _comparison()
                node = NodeExprBinary(token.location, operator, node, rhs)
            return node

        def _comparison() -> NodeExpr:
            '''
            term ( ("<" | ">" | "<=" | ">=") term)*;
            '''
            if self.debug_mode:
                print(f"[Parser::Expr::Binary::Comparison]")
            node = _term()
            while self._match(
                Token.Type.SymbolLt, Token.Type.SymbolGt,
                Token.Type.SymbolLtEq, Token.Type.SymbolGtEq
            ):
                token = self._last_token
                operator = OPERATOR_BINARY[token.type]
                rhs = _term()
                node = NodeExprBinary(token.location, operator, node, rhs)
            return node

        def _term() -> NodeExpr:
            '''
            factor ( ("+" | "-") factor)*;
            '''
            if self.debug_mode:
                print(f"[Parser::Expr::Binary::Term]")
            node = _factor()
            while self._match(Token.Type.SymbolPlus, Token.Type.SymbolMinus):
                token = self._last_token
                operator = OPERATOR_BINARY[token.type]
                rhs = _factor()
                node = NodeExprBinary(token.location, operator, node, rhs)
            return node

        def _factor() -> NodeExpr:
            '''
            expression_unary_prefix ( ("*" | "/" | "%") expression_unary_prefix)*;
            '''
            if self.debug_mode:
                print(f"[Parser::Expr::Binary::Factor]")
            node = self._parse_expression_unary_prefix()
            while self._match(
                Token.Type.SymbolStar, Token.Type.SymbolFSlash,
                Token.Type.SymbolPercent
            ):
                token = self._last_token
                operator = OPERATOR_BINARY[token.type]
                rhs = self._parse_expression_unary_prefix()
                node = NodeExprBinary(token.location, operator, node, rhs)
            return node

        # -Body
        return _equality()

    def _parse_expression_unary_prefix(self) -> NodeExpr:
        '''
        Grammar[Expression::Unary::Prefix]
        ('-' | '!') expression_unary_prefix | expression_unary_postfix;
        '''
        if self.debug_mode:
            print(f"[Parser::Expr::Unary::Prefix]")
        if self._match(*OPERATOR_UNARY.keys()):
            token = self._last_token
            operator = OPERATOR_UNARY[token.type]
            node = self._parse_expression_unary_prefix()
            return NodeExprUnary(token.location, operator, node)
        return self._parse_expression_unary_postfix()

    def _parse_expression_unary_postfix(self) -> NodeExpr:
        '''
        Grammar[Expression::Unary::Postfix]
        expression_primary (expression_unary_postfix_call)*;
        '''
        if self.debug_mode:
            print(f"[Parser::Expr::Unary::Postfix]")
        # -Internal Functions
        def _call(node: NodeExpr) -> NodeExpr:
            '''
            ( '(' (expression (',' expression)*)? ')' );
            '''
            if self.debug_mode:
                print(f"[Parser::Expr::Unary::Postfix::Call]")
            location = self._last_token.location
            arguments: list[NodeExpr] | None = None
            # -Arguments: 0
            if not self._consume(Token.Type.SymbolRParen):
                # -Arguments: 1
                arguments = [self._parse_expression()]
                # -Arguments: 2+
                while self._consume(Token.Type.SymbolComma):
                    arguments.append(self._parse_expression())
                # -TODO: Error Handling
                assert self._consume(Token.Type.SymbolRParen)
            return NodeExprCall(location, node, arguments)

        # -Body
        node = self._parse_expression_primary()
        # -Rule: Call
        while self._consume(Token.Type.SymbolLParen):
            node = _call(node)
        return node

    def _parse_expression_primary(self) -> NodeExpr:
        '''
        Grammar[Expression::Primary]
        IDENTIFIER | expression_literal | '(' expression ')';
        '''
        if self.debug_mode:
            print(f"[Parser::Expr::Primary]")
        # -Rule: Identifier
        if self._match(Token.Type.Identifier):
            token = self._last_token
            assert token.value is not None
            return NodeExprVariable(token.location, token.value)
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
        if self.debug_mode:
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
