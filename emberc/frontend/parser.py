##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Parser              ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Iterator
from .lookahead_buffer import LookaheadBuffer
from .token import Token
from ..ast import (
    BLOCK_TYPES,
    UnresolvedNode, UnresolvedUnitNode,
    UnresolvedTypeNode, UnresolvedDeclNode, UnresolvedStmtNode,
    UnresolvedDeclFunctionNode, UnresolvedDeclVariableNode,
    UnresolvedStmtBlockNode, UnresolvedStmtExpressionNode,
    UnresolvedStmtConditionalNode, UnresolvedStmtLoopWhileNode,
    UnresolvedStmtLoopDoNode, UnresolvedStmtLoopForNode,
    UnresolvedStmtReturnNode, UnresolvedStmtEmptyNode,
    UnresolvedGroupNode, UnresolvedExprEmptyNode,
    UnresolvedAssignNode, UnresolvedBinaryNode,
    UnresolvedUnaryPrefixNode, UnresolvedUnaryPostfixNode,
    UnresolvedIdentifierNode, UnresolvedLiteralNode, UnresolvedArrayNode
)
from ..location import Location

## Constants
LITERALS = (
    Token.Type.Boolean,
    Token.Type.Integer,
    Token.Type.String,
)
UNARY_PREFIX_OPERATORS = {
    Token.Type.SymbolMinus: UnresolvedUnaryPrefixNode.Operator.Negative,
    Token.Type.SymbolBang: UnresolvedUnaryPrefixNode.Operator.LogNeg,
    Token.Type.SymbolBitNeg: UnresolvedUnaryPrefixNode.Operator.BitNeg,
    Token.Type.SymbolStar: UnresolvedUnaryPrefixNode.Operator.Ptr,
    Token.Type.SymbolAt: UnresolvedUnaryPrefixNode.Operator.Ref,
    Token.Type.SymbolBitXor: UnresolvedUnaryPrefixNode.Operator.Deref,
}
UNARY_POSTFIX_OPERATORS = (
    Token.Type.SymbolLParen,
    Token.Type.SymbolLBracket,
)
BINARY_OPERATORS = {
    Token.Type.SymbolLogOr: (UnresolvedBinaryNode.Operator.LogOr, 1),
    Token.Type.SymbolLogAnd: (UnresolvedBinaryNode.Operator.LogAnd, 2),
    Token.Type.SymbolEqEq: (UnresolvedBinaryNode.Operator.Eq, 3),
    Token.Type.SymbolNtEq: (UnresolvedBinaryNode.Operator.NtEq, 3),
    Token.Type.SymbolLt: (UnresolvedBinaryNode.Operator.Lt, 4),
    Token.Type.SymbolGt: (UnresolvedBinaryNode.Operator.Gt, 4),
    Token.Type.SymbolLtEq: (UnresolvedBinaryNode.Operator.LtEq, 4),
    Token.Type.SymbolGtEq: (UnresolvedBinaryNode.Operator.GtEq, 4),
    Token.Type.SymbolDotDot: (UnresolvedBinaryNode.Operator.Range, 5),
    Token.Type.SymbolPlus: (UnresolvedBinaryNode.Operator.Add, 6),
    Token.Type.SymbolMinus: (UnresolvedBinaryNode.Operator.Sub, 6),
    Token.Type.SymbolBitOr: (UnresolvedBinaryNode.Operator.BitOr, 6),
    Token.Type.SymbolBitXor: (UnresolvedBinaryNode.Operator.BitXor, 6),
    Token.Type.SymbolStar: (UnresolvedBinaryNode.Operator.Mul, 7),
    Token.Type.SymbolFSlash: (UnresolvedBinaryNode.Operator.Div, 7),
    Token.Type.SymbolPercent: (UnresolvedBinaryNode.Operator.Mod, 7),
    Token.Type.SymbolBitAnd: (UnresolvedBinaryNode.Operator.BitAnd, 7),
    Token.Type.SymbolLShift: (UnresolvedBinaryNode.Operator.ShiftL, 8),
    Token.Type.SymbolRShift: (UnresolvedBinaryNode.Operator.ShiftR, 8),
}
ASSIGNMENT_OPERATORS = {
    Token.Type.SymbolEq: UnresolvedAssignNode.Operator.Eq,
    Token.Type.SymbolPlusEq: UnresolvedAssignNode.Operator.AddEq,
    Token.Type.SymbolMinusEq: UnresolvedAssignNode.Operator.SubEq,
    Token.Type.SymbolStarEq: UnresolvedAssignNode.Operator.MulEq,
    Token.Type.SymbolFSlashEq: UnresolvedAssignNode.Operator.DivEq,
    Token.Type.SymbolPercentEq: UnresolvedAssignNode.Operator.ModEq,
    Token.Type.SymbolBitNegEq: UnresolvedAssignNode.Operator.BitNegEq,
    Token.Type.SymbolBitXorEq: UnresolvedAssignNode.Operator.BitXorEq,
    Token.Type.SymbolBitAndEq: UnresolvedAssignNode.Operator.BitAndEq,
    Token.Type.SymbolBitOrEq: UnresolvedAssignNode.Operator.BitOrEq,
    Token.Type.SymbolLShiftEq: UnresolvedAssignNode.Operator.ShiftLEq,
    Token.Type.SymbolRShiftEq: UnresolvedAssignNode.Operator.ShiftREq,
}
TYPE_TABLE = {
    Token.Type.KeywordVoid: UnresolvedTypeNode.Type.Void,
    Token.Type.KeywordBoolean: UnresolvedTypeNode.Type.Boolean,
    Token.Type.KeywordInt8: UnresolvedTypeNode.Type.Int8,
    Token.Type.KeywordInt16: UnresolvedTypeNode.Type.Int16,
    Token.Type.KeywordInt32: UnresolvedTypeNode.Type.Int32,
    Token.Type.KeywordInt64: UnresolvedTypeNode.Type.Int64,
    Token.Type.KeywordUInt8: UnresolvedTypeNode.Type.UInt8,
    Token.Type.KeywordUInt16: UnresolvedTypeNode.Type.UInt16,
    Token.Type.KeywordUInt32: UnresolvedTypeNode.Type.UInt32,
    Token.Type.KeywordUInt64: UnresolvedTypeNode.Type.UInt64,
}
EXPRESSION_STARTERS = (
    Token.Type.Identifier, *LITERALS,
    Token.Type.SymbolLParen, *UNARY_PREFIX_OPERATORS.keys(),
    *TYPE_TABLE.keys(),
)
EXPRESSION_TERMINATORS = (
    Token.Type.SymbolComma,
    Token.Type.SymbolRBracket,
    Token.Type.SymbolSemicolon,
)
STATEMENT_STARTERS = (
    Token.Type.KeywordIf,
    Token.Type.KeywordWhile,
    Token.Type.KeywordDo,
    Token.Type.KeywordFor,
    Token.Type.KeywordReturn,
    Token.Type.SymbolSemicolon,
    Token.Type.SymbolLBrace,
)


## Functions
def _create_literal_node(token: Token) -> UnresolvedLiteralNode:
    """Helper function for creating node literals by type"""
    match token.type:
        case Token.Type.Boolean:
            assert isinstance(token.value, bool)
            return UnresolvedLiteralNode(
                token.location, token.value, UnresolvedLiteralNode.Type.Boolean
            )
        case Token.Type.Integer:
            assert isinstance(token.value, int)
            return UnresolvedLiteralNode(
                token.location, token.value, UnresolvedLiteralNode.Type.Integer
            )
        case Token.Type.String:
            assert isinstance(token.value, str)
            return UnresolvedLiteralNode(
                token.location, token.value, UnresolvedLiteralNode.Type.String
            )
        case _:
            raise NotImplementedError(f"Token.Type {token.type.name} not handled in _create_literal")


def _create_range_binary_operator(
    parser: Parser, location: Location, precedence: int
) -> UnresolvedNode:
    """Helper function for handling parsing range infix binary"""
    if parser.matches(*EXPRESSION_TERMINATORS):
        return UnresolvedExprEmptyNode(location)
    return parser._parse_expression_binary(precedence)


## Classes
class Parser(LookaheadBuffer[Token, Token.Type]):
    """
    Ember Parser: Lookahead(n)

    Handles iterating over a token stream and produces an unresolved
    and ambigious Ember AST. Later passes must sort and contextualize
    the AST into resolved nodes.
    """

    # -Constructor
    def __init__(self, token_iter: Iterator[Token]) -> None:
        super().__init__(token_iter, lambda token: token.type)
        self._last_token: Token

    # -Instance Methods: Lookahead
    def advance(self) -> Token | None:
        token = super().advance()
        if token:
            self._last_token = token
        return token

    def require(self, expected: Token.Type) -> Token:
        '''Raises ParserError if next token is not expected type'''
        if self.consume(expected):
            return self._last_token
        assert False, "TODO: Error handling"

    def require_any(self, *expected: Token.Type) -> Token:
        '''Raises ParserError if next token is not in expected types'''
        if self.matches(*expected):
            token = self.advance()
            assert token is not None
            return token
        assert False, "TODO: Error handling"

    # -Instance Methods: Parser
    def parse(self) -> UnresolvedUnitNode:
        '''
        Grammar[Unit]
        declaration*;
        '''
        declarations: list[UnresolvedNode] = []
        while not self.is_at_end:
            decl = self._parse_declaration()
            declarations.append(decl)
        return UnresolvedUnitNode(declarations)

    def _try_parse_type(self) -> tuple[bool, UnresolvedNode]:
        '''Tries parsing a type and returns True if considered decl scope'''
        expr = self._parse_type()
        is_decl = self.match(Token.Type.Identifier)
        return (is_decl, expr)

    def _parse_type(self) -> UnresolvedNode:
        '''Returns either a parsed type or partially parsed expression'''
        return self._parse_unary_prefix()

    def _parse_declaration(self) -> UnresolvedNode:
        '''
        Grammar[Declaration]
        declaration_function | declaration_variable;
        '''
        if self.match(Token.Type.KeywordFn):
            return self._parse_declaration_function()
        return self._parse_declaration_variable()

    def _parse_declaration_function(self) -> UnresolvedDeclFunctionNode:
        '''
        Grammar[Declaration:Function]
        'fn' IDENTIFIER '(' (parameter (',' parameter)*)? ')' ':' TYPE '{' declaration_statement* '}'
        '''
        # -Internal Methods
        def _parse_parameter() -> UnresolvedDeclFunctionNode.Parameter:
            '''parameter: TYPE IDENTIFIER ('=' expression)?;'''
            _type = self._parse_type()
            ident = self.require(Token.Type.Identifier)
            assert isinstance(ident.value, str)
            initializer: UnresolvedNode | None = None
            if self.consume(Token.Type.SymbolEq):
                initializer = self._parse_expression()
            return UnresolvedDeclFunctionNode.Parameter(_type, ident.value, initializer)
        # -Body
        token = self.require(Token.Type.KeywordFn)
        ident = self.require(Token.Type.Identifier)
        assert isinstance(ident.value, str)
        self.require(Token.Type.SymbolLParen)
        parameters: list[UnresolvedDeclFunctionNode.Parameter] = []
        # -Params: Zero
        if not self.consume(Token.Type.SymbolRParen):
            # -Params: One
            parameters.append(_parse_parameter())
            # -Params: Multi
            while self.consume(Token.Type.SymbolComma):
                parameters.append(_parse_parameter())
            self.require(Token.Type.SymbolRParen)
        self.require(Token.Type.SymbolColon)
        _type = self._parse_type()
        body = self._parse_statement_block()
        return UnresolvedDeclFunctionNode(
            token.location, ident.value, parameters, _type, body
        )

    def _parse_declaration_statement(self) -> UnresolvedDeclNode | UnresolvedStmtNode:
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

    def _parse_declaration_variable(
        self, head: UnresolvedNode | None = None
    ) -> UnresolvedDeclVariableNode:
        '''
        Grammar[Declaration:Variable]
        TYPE entry ( ',' entry )* ';';

        entry: IDENTIFIER ( '=' expression )?;
        '''
        # -Internal Methods
        def _parse_entry() -> UnresolvedDeclVariableNode.Entry:
            ident = self.require(Token.Type.Identifier)
            assert isinstance(ident.value, str)
            initializer: UnresolvedNode | None = None
            if self.consume(Token.Type.SymbolEq):
                initializer = self._parse_expression()
            return UnresolvedDeclVariableNode.Entry(
                ident.location, ident.value, initializer
            )
        # -Body
        if head is None:
            head = self._parse_type()
        # -One
        entries: list[UnresolvedDeclVariableNode.Entry] = [_parse_entry()]
        # -Multi
        while self.consume(Token.Type.SymbolComma):
            entries.append(_parse_entry())
        self.require(Token.Type.SymbolSemicolon)
        return UnresolvedDeclVariableNode(head.location, head, entries)

    def _parse_statement(self) -> UnresolvedStmtNode:
        '''
        Grammar[Statement]
        statement_empty | statement_block | statement_loop | statement_expression;

        statement_loop: statement_loop_while | statement_loop_do | statement_loop_for;
        '''
        # -Statement: Empty
        if self.consume(Token.Type.SymbolSemicolon):
            return UnresolvedStmtEmptyNode(self.last_location)
        # -Statement: Block
        elif self.match(Token.Type.SymbolLBrace):
            return self._parse_statement_block()
        # -Statement: Conditional
        elif self.match(Token.Type.KeywordIf):
            return self._parse_statement_conditional()
        # -Statement: Loop - While
        elif self.match(Token.Type.KeywordWhile):
            return self._parse_statement_loop_while()
        # -Statement: Loop - Do
        elif self.match(Token.Type.KeywordDo):
            return self._parse_statement_loop_do()
        # -Statement: Loop - For
        elif self.match(Token.Type.KeywordFor):
            return self._parse_statement_loop_for()
        # -Statement: Return
        elif self.match(Token.Type.KeywordReturn):
            return self._parse_statement_return()
        # -Statement: Expression
        return self._parse_statement_expression()

    def _parse_statement_block(self) -> UnresolvedStmtBlockNode:
        '''
        Grammar[Statement:Block]
        '{' declaration_statement '}';
        '''
        token = self.require(Token.Type.SymbolLBrace)
        body: list[BLOCK_TYPES] = []
        while not self.match(Token.Type.SymbolRBrace) and not self.is_at_end:
            elem = self._parse_declaration_statement()
            body.append(elem)
        self.require(Token.Type.SymbolRBrace)
        return UnresolvedStmtBlockNode(token.location, body)

    def _parse_statement_conditional(self) -> UnresolvedStmtConditionalNode:
        '''
        Grammar[Statement:Conditional]
        if '(' expression ')' statement ( 'else' statement )?;
        '''
        token = self.require(Token.Type.KeywordIf)
        self.require(Token.Type.SymbolLParen)
        condition = self._parse_expression()
        self.require(Token.Type.SymbolRParen)
        if_branch = self._parse_statement()
        else_branch: UnresolvedStmtNode | None = None
        if self.consume(Token.Type.KeywordElse):
            else_branch = self._parse_statement()
        return UnresolvedStmtConditionalNode(
            token.location, condition, if_branch, else_branch
        )

    def _parse_statement_loop_while(self) -> UnresolvedStmtLoopWhileNode:
        '''
        Grammar[Statement:Loop:While]
        while '(' expression ')' statement;
        '''
        token = self.require(Token.Type.KeywordWhile)
        self.require(Token.Type.SymbolLParen)
        condition = self._parse_expression()
        self.require(Token.Type.SymbolRParen)
        body = self._parse_statement()
        return UnresolvedStmtLoopWhileNode(token.location, condition, body)

    def _parse_statement_loop_do(self) -> UnresolvedStmtLoopDoNode:
        '''
        Grammar[Statement:Loop:While]
        do statement while '(' expression ')' ';';
        '''
        token = self.require(Token.Type.KeywordDo)
        body = self._parse_statement()
        self.require(Token.Type.KeywordWhile)
        self.require(Token.Type.SymbolLParen)
        condition = self._parse_expression()
        self.require(Token.Type.SymbolRParen)
        self.require(Token.Type.SymbolSemicolon)
        return UnresolvedStmtLoopDoNode(token.location, condition, body)

    def _parse_statement_loop_for(self) -> UnresolvedStmtLoopForNode:
        '''
        Grammar[Statement:Loop:For]
        'for' '(' (declaration_variable | expression? ';') expression? ';' expression? ')' statement;
        '''
        token = self.require(Token.Type.KeywordFor)
        self.require(Token.Type.SymbolLParen)
        # -<Initializer>-
        initializer: UnresolvedNode | None = None
        if not self.consume(Token.Type.SymbolSemicolon):
            is_decl, node = self._try_parse_type()
            if is_decl:
                initializer = self._parse_declaration_variable(node)
            else:
                initializer = self._parse_expression(node)
                self.require(Token.Type.SymbolSemicolon)
        # -<Condition>-
        condition: UnresolvedNode
        if not self.consume(Token.Type.SymbolSemicolon):
            condition = self._parse_expression()
            self.require(Token.Type.SymbolSemicolon)
        else:
            condition = UnresolvedLiteralNode(
                self.last_location, True, UnresolvedLiteralNode.Type.Boolean
            )
        # -<Increment>-
        increment: UnresolvedNode | None = None
        if not self.match(Token.Type.SymbolRParen):
            increment = self._parse_expression()
        # -<Body>-
        self.require(Token.Type.SymbolRParen)
        body = self._parse_statement()
        return UnresolvedStmtLoopForNode(
            token.location, initializer, condition, increment, body
        )

    def _parse_statement_return(self) -> UnresolvedStmtReturnNode:
        '''
        Grammar[Statement:Return]
        return expression? ';';
        '''
        token = self.require(Token.Type.KeywordReturn)
        value: UnresolvedNode | None = None
        if not self.consume(Token.Type.SymbolSemicolon):
            value = self._parse_expression()
            self.require(Token.Type.SymbolSemicolon)
        return UnresolvedStmtReturnNode(token.location, value)

    def _parse_statement_expression(
        self, head: UnresolvedNode | None = None
    ) -> UnresolvedStmtExpressionNode:
        '''
        Grammar[Statement:Expression]
        expression ';';
        '''
        if head is not None and self.consume(Token.Type.SymbolSemicolon):
            return UnresolvedStmtExpressionNode(self.last_location, head)
        head = self._parse_expression(head)
        self.require(Token.Type.SymbolSemicolon)
        return UnresolvedStmtExpressionNode(self.last_location, head)

    def _parse_expression(
        self, head: UnresolvedNode | None = None
    ) -> UnresolvedNode:
        '''
        Grammar[Expression]
        expression_binary (ASSIGNMENT_OPERATOR expression_binary)?;
        '''
        l_value = self._parse_expression_binary(lhs=head)
        if self.matches(*ASSIGNMENT_OPERATORS.keys()):
            token = self.next()
            operator = ASSIGNMENT_OPERATORS[token.type]
            r_value = self._parse_expression()
            l_value = UnresolvedAssignNode(token.location, operator, l_value, r_value)
        return l_value

    def _parse_expression_binary(
        self, current: int = 0, lhs: UnresolvedNode | None = None
    ) -> UnresolvedNode:
        '''
        Grammar[Expression:Binary]
        unary_prefix (BINARY_OPERATOR expression_binary)*;
        '''
        if lhs is None:
            lhs = self._parse_unary_prefix()
        while self.matches(*BINARY_OPERATORS.keys()):
            token = self.current
            operator, precedence = BINARY_OPERATORS[token.type]
            if precedence <= current:
                break
            token = self.next()
            rhs: UnresolvedNode
            if operator == UnresolvedBinaryNode.Operator.Range:
                rhs = _create_range_binary_operator(
                    self, token.location, precedence
                )
            else:
                rhs = self._parse_expression_binary(precedence)
            lhs = UnresolvedBinaryNode(token.location, operator, lhs, rhs)
        return lhs

    def _parse_unary_prefix(self) -> UnresolvedNode:
        '''
        Grammar[Unary]
        UNARY_PREFIX unary_prefix | primary;
        '''
        # -Unary: Range
        if self.consume(Token.Type.SymbolDotDot):
            token = self._last_token
            bin_operator, precedence = BINARY_OPERATORS[token.type]
            lhs = UnresolvedExprEmptyNode(token.location)
            rhs = _create_range_binary_operator(self, token.location, precedence)
            return UnresolvedBinaryNode(token.location, bin_operator, lhs, rhs)
        # -Unary: Slice
        if self.match(Token.Type.SymbolLBracket):
            next = self.peek(1)
            if next and next.type in (Token.Type.SymbolStar, Token.Type.SymbolRBracket):
                token = self.next()
                _type = UnresolvedUnaryPrefixNode.Operator.Slice
                if not self.consume(Token.Type.SymbolRBracket):
                    self.require(Token.Type.SymbolStar)
                    _type = UnresolvedUnaryPrefixNode.Operator.SlicePtr
                    self.require(Token.Type.SymbolRBracket)
                operand = self._parse_unary_prefix()
                return UnresolvedUnaryPrefixNode(token.location, _type, operand)
        # -Unary: Base
        elif self.matches(*UNARY_PREFIX_OPERATORS.keys()):
            token = self.next()
            operator = UNARY_PREFIX_OPERATORS[token.type]
            operand = self._parse_unary_prefix()
            return UnresolvedUnaryPrefixNode(token.location, operator, operand)
        # -Primary
        return self._parse_primary()

    def _parse_primary(self) -> UnresolvedNode:
        '''
        Grammar[Primary]
        primary_group | primary_array | literal;
        '''
        # -Group
        if self.match(Token.Type.SymbolLParen):
            return self._parse_primary_group()
        # -Array
        elif self.match(Token.Type.SymbolLBracket):
            return self._parse_primary_array()
        # -Literal
        node = self._parse_literal()
        return self._parse_unary_postfix(node)

    def _parse_primary_group(self) -> UnresolvedGroupNode:
        '''
        Grammar[Primary:Group]
        '(' expression ')';
        '''
        token = self.require(Token.Type.SymbolLParen)
        inner = self._parse_expression()
        self.require(Token.Type.SymbolRParen)
        inner = self._parse_unary_postfix(inner)
        node = UnresolvedGroupNode(token.location, inner)
        if self.matches(*EXPRESSION_STARTERS):
            node._target = self._parse_unary_prefix()
        return node

    def _parse_primary_array(self) -> UnresolvedArrayNode:
        '''
        Grammar[Primary:Array]
        '[' expression ( ',' expression )* ']';
        '''
        # -Body
        token = self.require(Token.Type.SymbolLBracket)
        values: list[UnresolvedNode] = [self._parse_expression()]
        while self.consume(Token.Type.SymbolComma):
            values.append(self._parse_expression())
        self.require(Token.Type.SymbolRBracket)
        return UnresolvedArrayNode(token.location, values)

    def _parse_unary_postfix(self, head: UnresolvedNode) -> UnresolvedNode:
        '''
        Grammar[Unary:Postfix]
        expression ( unary_call | unary_subscript)*;
        '''
        while self.matches(*UNARY_POSTFIX_OPERATORS):
            token = self.current
            match token.type:
                case Token.Type.SymbolLParen:
                    head = self._parse_unary_call(head)
                case Token.Type.SymbolLBracket:
                    head = self._parse_unary_subscript(head)
        return head

    def _parse_unary_call(self, head: UnresolvedNode) -> UnresolvedNode:
        '''
        Grammar[Unary:Postfix:Call]
        '(' ( expression ( ',' expression )* )? ')'
        '''
        token = self.require(Token.Type.SymbolLParen)
        # -Arguments: Zero
        arguments: list[UnresolvedNode] = []
        if not self.consume(Token.Type.SymbolRParen):
            # -Arguments: One
            arguments.append(self._parse_expression())
            # -Arguments: Multi
            while self.consume(Token.Type.SymbolComma):
                arguments.append(self._parse_expression())
            self.require(Token.Type.SymbolRParen)
        return UnresolvedUnaryPostfixNode(
            token.location, head,
            UnresolvedUnaryPostfixNode.Kind.Call, arguments
        )

    def _parse_unary_subscript(self, head: UnresolvedNode) -> UnresolvedNode:
        '''
        Grammar[Unary:Postfix:Subscript]
        '[' ( expression? ( ',' expression? )* )? ']'
        '''
        # -Internal Functions
        def _parse_argument() -> UnresolvedNode:
            if self.match(Token.Type.SymbolComma):
                return UnresolvedExprEmptyNode(token.location)
            elif self.match(Token.Type.SymbolRBracket):
                return UnresolvedExprEmptyNode(self.last_location)
            return self._parse_expression()
        # -Body
        token = self.require(Token.Type.SymbolLBracket)
        # -Arguments: One
        arguments: list[UnresolvedNode] = [_parse_argument()]
        # -Arguments: Multi
        while self.consume(Token.Type.SymbolComma):
            arguments.append(_parse_argument())
        self.require(Token.Type.SymbolRBracket)
        return UnresolvedUnaryPostfixNode(
            token.location, head,
            UnresolvedUnaryPostfixNode.Kind.Subscript, arguments
        )

    def _parse_literal(self) -> UnresolvedNode:
        '''
        Grammar[Literal]
        TYPE | IDENTIFIER | BOOL | INTEGER;
        '''
        # -Types
        if self.matches(*TYPE_TABLE.keys()):
            token = self.next()
            _type = TYPE_TABLE[token.type]
            return UnresolvedTypeNode(token.location, _type)
        # -Identifier
        elif self.match(Token.Type.Identifier):
            token = self.next()
            assert isinstance(token.value, str)
            return UnresolvedIdentifierNode(token.location, token.value)
        # -Literals
        token = self.require_any(*LITERALS)
        return _create_literal_node(token)

    # -Properties
    @property
    def is_at_end(self) -> bool:
        return self.peek() is None

    @property
    def last_location(self) -> Location:
        return self._last_token.location
