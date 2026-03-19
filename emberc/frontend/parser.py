##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Parser              ##
##-------------------------------##

## Imports
from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING
from .token import Token
from ..core import Location, LookaheadBuffer
from ..ast import (
    UnresolvedTypeNode,
    UnresolvedModifierNode,
    UnresolvedUnitNode,
    UnresolvedFunctionNode,
    UnresolvedVariableNode,
    UnresolvedBlockNode,
    UnresolvedConditionalNode,
    UnresolvedWhileNode,
    UnresolvedDoNode,
    UnresolvedForNode,
    UnresolvedFlowNode,
    UnresolvedReturnNode,
    UnresolvedExprNode,
    UnresolvedGroupNode,
    UnresolvedAssignmentNode,
    UnresolvedBinaryNode,
    UnresolvedUnaryPrefixNode,
    UnresolvedUnaryPostfixNode,
    UnresolvedLiteralNode,
    UnresolvedIdentifierNode,
    UnresolvedEmptyNode,
)

if TYPE_CHECKING:
    from collections.abc import Iterator
    from .lexer import Lexer
    from ..ast import AST_LITERAL_TYPES, UnresolvedNode

## Constants
LITERALS = (
    Token.Type.Boolean,
    Token.Type.Integer,
)
TYPES = {
    Token.Type.KeywordVoid: UnresolvedTypeNode.Kind.Void,
    Token.Type.KeywordBoolean: UnresolvedTypeNode.Kind.Boolean,
    Token.Type.KeywordInt8: UnresolvedTypeNode.Kind.Int8,
    Token.Type.KeywordInt16: UnresolvedTypeNode.Kind.Int16,
    Token.Type.KeywordInt32: UnresolvedTypeNode.Kind.Int32,
    Token.Type.KeywordInt64: UnresolvedTypeNode.Kind.Int64,
    Token.Type.KeywordUInt8: UnresolvedTypeNode.Kind.UInt8,
    Token.Type.KeywordUInt16: UnresolvedTypeNode.Kind.UInt16,
    Token.Type.KeywordUInt32: UnresolvedTypeNode.Kind.UInt32,
    Token.Type.KeywordUInt64: UnresolvedTypeNode.Kind.UInt64,
}
UNARY_PREFIX_OPERATORS = {
    Token.Type.SymbolMinus: UnresolvedUnaryPrefixNode.Operator.NumericalNegate,
    Token.Type.SymbolBang: UnresolvedUnaryPrefixNode.Operator.LogicalNegate,
    Token.Type.SymbolBitNeg: UnresolvedUnaryPrefixNode.Operator.BitwiseNegate,
    Token.Type.SymbolStar: UnresolvedUnaryPrefixNode.Operator.Pointer,
    Token.Type.SymbolAt: UnresolvedUnaryPrefixNode.Operator.AddressOf,
}
UNARY_PREFIX_MODIFIERS = {
    Token.Type.KeywordConst: UnresolvedModifierNode.Kind.Const,
}
UNARY_POSTFIX_OPERATORS = (
    Token.Type.SymbolDot,
    Token.Type.SymbolLParen,
)
BINARY_OPERATORS = {
    Token.Type.KeywordOr: (UnresolvedBinaryNode.Operator.LogOr, 1),
    Token.Type.KeywordAnd: (UnresolvedBinaryNode.Operator.LogAnd, 2),
    Token.Type.SymbolEqEq: (UnresolvedBinaryNode.Operator.Eq, 3),
    Token.Type.SymbolNtEq: (UnresolvedBinaryNode.Operator.NtEq, 3),
    Token.Type.SymbolLt: (UnresolvedBinaryNode.Operator.Lt, 4),
    Token.Type.SymbolGt: (UnresolvedBinaryNode.Operator.Gt, 4),
    Token.Type.SymbolLtEq: (UnresolvedBinaryNode.Operator.LtEq, 4),
    Token.Type.SymbolGtEq: (UnresolvedBinaryNode.Operator.GtEq, 4),
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
    Token.Type.SymbolEq: UnresolvedAssignmentNode.Operator.Eq,
    Token.Type.SymbolPlusEq: UnresolvedAssignmentNode.Operator.AddEq,
    Token.Type.SymbolMinusEq: UnresolvedAssignmentNode.Operator.SubEq,
    Token.Type.SymbolStarEq: UnresolvedAssignmentNode.Operator.MulEq,
    Token.Type.SymbolFSlashEq: UnresolvedAssignmentNode.Operator.DivEq,
    Token.Type.SymbolPercentEq: UnresolvedAssignmentNode.Operator.ModEq,
    Token.Type.SymbolBitXorEq: UnresolvedAssignmentNode.Operator.BitXorEq,
    Token.Type.SymbolBitAndEq: UnresolvedAssignmentNode.Operator.BitAndEq,
    Token.Type.SymbolBitOrEq: UnresolvedAssignmentNode.Operator.BitOrEq,
    Token.Type.SymbolLShiftEq: UnresolvedAssignmentNode.Operator.ShiftLEq,
    Token.Type.SymbolRShiftEq: UnresolvedAssignmentNode.Operator.ShiftREq,
}
EXPRESSION_STARTERS = (
    Token.Type.Identifier,
    *LITERALS,
    *UNARY_PREFIX_OPERATORS.keys(),
)
STATEMENT_STARTERS = (
    Token.Type.SymbolSemicolon,
    Token.Type.SymbolLBrace,
    Token.Type.KeywordIf,
    Token.Type.KeywordWhile,
    Token.Type.KeywordDo,
    Token.Type.KeywordFor,
    Token.Type.KeywordBreak,
    Token.Type.KeywordContinue,
    Token.Type.KeywordReturn,
)


## Classes
class Parser(LookaheadBuffer[Token, Token.Type]):
    """
    Ember Lookahead(n) Parser

    Transforms a linear stream of tokens into a structural AST.
    Produces an unresolved, ambiguous tree that serves as the
    foundation for later semantic analysis and symbol resolution.
    """

    # -Constructor
    def __init__(self, source: Iterator[Token]) -> None:
        super().__init__(source, lambda token: token.type)
        self._last_token: Token
        self.file: Path | None = None

    # -Instance Methods: Lookahead
    def advance(self) -> Token | None:
        token = super().advance()
        if token:
            self._last_token = token
        return token

    def require(self, expected: Token.Type) -> Token:
        '''Raises error if next token is not expected type'''
        if self.consume(expected):
            return self._last_token
        assert False, "TODO: Error handling"

    def requires(self, *expected: Token.Type) -> Token:
        '''Returns next token if in expected types; raises error otherwise'''
        if self.matches(*expected):
            return self.next()
        expected_str = ','.join(_type.name for _type in expected)
        assert False, "TODO: Error handling"

    # -Instance Methods: Parser
    def parse(self) -> UnresolvedUnitNode:
        '''
        Grammar[Unit]
        statement*;
        '''
        nodes: list[UnresolvedNode] = []
        while not self.is_at_end:
            node = self._parse_declaration()
            nodes.append(node)
        return UnresolvedUnitNode(Location(self.file, (0, 0, 0)), nodes)

    def _parse_declaration(self) -> UnresolvedNode:
        '''
        Grammar[Declaration]
        declaration_function | declaration_variable;
        '''
        if self.matches(Token.Type.KeywordFn):
            return self._parse_declaration_function()
        return self._parse_declaration_variable()

    def _parse_declaration_function(self) -> UnresolvedNode:
        '''
        Grammar[Declaration::Function]
        'fn' IDENTIFIER '(' ( parameter ( ',' parameter )* )? ')' ':' TYPE statement_block;
        '''
        # -Internal Functions
        def _parse_paramater() -> UnresolvedFunctionNode.Parameter:
            '''TYPE IDENTIFIER ( '=' expression )?;'''
            _type = self._parse_expression_unary_prefix()
            ident = self.require(Token.Type.Identifier)
            initializer: UnresolvedNode | None = None
            if self.consume(Token.Type.SymbolEq):
                initializer = self._parse_expression()
            return UnresolvedFunctionNode.Parameter(
                _type, ident.value_as(str), initializer
            )
        # -Body
        token = self.require(Token.Type.KeywordFn)
        ident = self.require(Token.Type.Identifier)
        _ = self.require(Token.Type.SymbolLParen)
        parameters: list[UnresolvedFunctionNode.Parameter] = []
        # -Parameters: Zero
        if not self.consume(Token.Type.SymbolRParen):
            # -Parameters: One
            parameters.append(_parse_paramater())
            # -Parameters: Multi
            while self.consume(Token.Type.SymbolComma):
                parameters.append(_parse_paramater())
            _ = self.require(Token.Type.SymbolRParen)
        _ = self.require(Token.Type.SymbolColon)
        return_type = self._parse_expression_unary_prefix()
        body = self._parse_statement_block()
        return UnresolvedFunctionNode(
            token.location, ident.value_as(str), parameters, return_type, body
        )

    def _parse_declaration_variable(
        self, _type: UnresolvedNode | None = None
    ) -> UnresolvedNode:
        '''
        Grammar[Declaration::Variable]
        TYPE entry ( ',' entry )* ';';
        '''
        # -Internal Functions
        def _parse_entry() -> UnresolvedVariableNode.Entry:
            '''IDENTIFIER ( '=' expression )?;'''
            token = self.require(Token.Type.Identifier)
            initializer: UnresolvedNode | None = None
            if self.consume(Token.Type.SymbolEq):
                initializer = self._parse_expression()
            return UnresolvedVariableNode.Entry(
                token.location, token.value_as(str), initializer
            )
        # -Body
        if _type is None:
            _type = self._parse_expression_unary_prefix()
        # -Entry: One
        entries: list[UnresolvedVariableNode.Entry] = [_parse_entry()]
        # -Entry: Multi
        while self.consume(Token.Type.SymbolComma):
            entries.append(_parse_entry())
        _ = self.require(Token.Type.SymbolSemicolon)
        return UnresolvedVariableNode(_type.location, _type, entries)

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
        statement_block | statement_conditional | statement_while | statement_do | statement_for | statement_expression;
        '''
        if self.matches(Token.Type.SymbolLBrace):
            return self._parse_statement_block()
        elif self.matches(Token.Type.KeywordIf):
            return self._parse_statement_conditional()
        elif self.matches(Token.Type.KeywordWhile):
            return self._parse_statement_loop_while()
        elif self.matches(Token.Type.KeywordDo):
            return self._parse_statement_loop_do()
        elif self.matches(Token.Type.KeywordFor):
            return self._parse_statement_loop_for()
        elif self.matches(Token.Type.KeywordBreak):
            return self._parse_statement_break()
        elif self.matches(Token.Type.KeywordContinue):
            return self._parse_statement_continue()
        elif self.matches(Token.Type.KeywordReturn):
            return self._parse_statement_return()
        return self._parse_statement_expression()

    def _parse_statement_block(self) -> UnresolvedNode:
        '''
        Grammar[Statement::Block]
        '{' declaration_statement* '}';
        '''
        token = self.require(Token.Type.SymbolLBrace)
        nodes: list[UnresolvedNode] = []
        while not self.is_at_end and not self.consume(Token.Type.SymbolRBrace):
            node = self._parse_declaration_statement()
            nodes.append(node)
        return UnresolvedBlockNode(token.location, nodes)

    def _parse_statement_conditional(self) -> UnresolvedNode:
        '''
        Grammar[Statement::Conditional]
        'if' '(' expression ')' statement ( 'else' statement )?;
        '''
        token = self.require(Token.Type.KeywordIf)
        _ = self.require(Token.Type.SymbolLParen)
        condition = self._parse_expression()
        _ = self.require(Token.Type.SymbolRParen)
        if_branch = self._parse_statement()
        else_branch: UnresolvedNode | None = None
        if self.consume(Token.Type.KeywordElse):
            else_branch = self._parse_statement()
        return UnresolvedConditionalNode(
            token.location, condition, if_branch, else_branch
        )

    def _parse_statement_loop_while(self) -> UnresolvedNode:
        '''
        Grammar[Statement::Loop::While]
        'while' '(' expression ')' statement;
        '''
        token = self.require(Token.Type.KeywordWhile)
        _ = self.require(Token.Type.SymbolLParen)
        condition = self._parse_expression()
        _ = self.require(Token.Type.SymbolRParen)
        body = self._parse_statement()
        return UnresolvedWhileNode(token.location, condition, body)

    def _parse_statement_loop_do(self) -> UnresolvedNode:
        '''
        Grammar[Statement::Loop:Do]
        'do' statement 'while' '(' expression ')';
        '''
        token = self.require(Token.Type.KeywordDo)
        body = self._parse_statement()
        _ = self.require(Token.Type.KeywordWhile)
        _ = self.require(Token.Type.SymbolLParen)
        condition = self._parse_expression()
        _ = self.require(Token.Type.SymbolRParen)
        _ = self.require(Token.Type.SymbolSemicolon)
        return UnresolvedDoNode(token.location, condition, body)

    def _parse_statement_loop_for(self) -> UnresolvedNode:
        '''
        Grammar[Statement::Loop::For]
        'for' '(' ( declaration_variable | expression? ';' ) expression? ';' expression? ')' statement;
        '''
        token = self.require(Token.Type.KeywordFor)
        _ = self.require(Token.Type.SymbolLParen)
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
        condition: UnresolvedNode = UnresolvedLiteralNode(
            self._last_token.location,
            UnresolvedLiteralNode.Kind.Boolean,
            True
        )
        if not self.consume(Token.Type.SymbolSemicolon):
            condition = self._parse_expression()
            self.require(Token.Type.SymbolSemicolon)
        # -<Increment>-
        increment: UnresolvedNode | None = None
        if not self.matches(Token.Type.SymbolRParen):
            increment = self._parse_expression()
        # -<Body>-
        self.require(Token.Type.SymbolRParen)
        body = self._parse_statement()
        return UnresolvedForNode(
            token.location, initializer, condition, increment, body
        )

    def _parse_statement_break(self) -> UnresolvedNode:
        '''
        Grammar[Statement::Break]
        'break' ';';
        '''
        token = self.require(Token.Type.KeywordBreak)
        _ = self.require(Token.Type.SymbolSemicolon)
        return UnresolvedFlowNode(
            token.location, UnresolvedFlowNode.Kind.Break
        )

    def _parse_statement_continue(self) -> UnresolvedNode:
        '''
        Grammar[Statement::Continue]
        'continue' ';';
        '''
        token = self.require(Token.Type.KeywordContinue)
        _ = self.require(Token.Type.SymbolSemicolon)
        return UnresolvedFlowNode(
            token.location, UnresolvedFlowNode.Kind.Continue
        )

    def _parse_statement_return(self) -> UnresolvedNode:
        '''
        Grammar[Statement::Return]
        'return' expression? ';';
        '''
        token = self.require(Token.Type.KeywordReturn)
        expression: UnresolvedNode | None = None
        if not self.consume(Token.Type.SymbolSemicolon):
            expression = self._parse_expression()
            _ = self.require(Token.Type.SymbolSemicolon)
        return UnresolvedReturnNode(token.location, expression)

    def _parse_statement_expression(
        self, expr: UnresolvedNode | None = None
    ) -> UnresolvedNode:
        '''
        Grammar[Statement::Expression]
        expression? ';';
        '''
        if expr is None and self.consume(Token.Type.SymbolSemicolon):
            return UnresolvedExprNode(self._last_token.location, None)
        node = self._parse_expression(expr)
        token = self.require(Token.Type.SymbolSemicolon)
        return UnresolvedExprNode(token.location, node)

    def _parse_expression(
        self, l_value: UnresolvedNode | None = None
    ) -> UnresolvedNode:
        '''
        Grammar[Expression]
        expression_binary ( ASSIGNMENT_OPERATOR expression )?;
        '''
        l_value = self._parse_expression_binary(lhs=l_value)
        if self.matches(*ASSIGNMENT_OPERATORS.keys()):
            token = self.next()
            operator = ASSIGNMENT_OPERATORS[token.type]
            r_value = self._parse_expression()
            l_value = UnresolvedAssignmentNode(token.location, operator, l_value, r_value)
        return l_value

    def _parse_expression_binary(
        self, current: int = 0, lhs: UnresolvedNode | None = None
    ) -> UnresolvedNode:
        '''
        Grammar[Expression::Binary]
        expression_unary_prefix ( BINARY_OPERATOR expression_binary )*;
        '''
        if lhs is None:
            lhs = self._parse_expression_unary_prefix()
        while self.matches(*BINARY_OPERATORS.keys()):
            token = self.current
            operator, precedence = BINARY_OPERATORS[token.type]
            if precedence <= current:
                break
            token = self.next()
            rhs = self._parse_expression_binary(precedence)
            lhs = UnresolvedBinaryNode(token.location, operator, lhs, rhs)
        return lhs

    def _parse_expression_unary_prefix(self) -> UnresolvedNode:
        '''
        Grammar[Expression::Unary::Prefix]
        UNARY_PREFIX_OPERATOR expression_unary_prefix | primary;
        '''
        # -Operators
        if self.matches(*UNARY_PREFIX_OPERATORS.keys()):
            token = self.next()
            operator = UNARY_PREFIX_OPERATORS[token.type]
            operand = self._parse_expression_unary_prefix()
            return UnresolvedUnaryPrefixNode(token.location, operator, operand)
        # -Modifiers
        elif self.matches(*UNARY_PREFIX_MODIFIERS.keys()):
            token = self.next()
            modifier = UNARY_PREFIX_MODIFIERS[token.type]
            target = self._parse_expression_unary_prefix()
            return UnresolvedModifierNode(token.location, modifier, target)
        return self._parse_expression_primary()

    def _parse_expression_unary_postfix(
        self, head: UnresolvedNode
    ) -> UnresolvedNode:
        '''
        Grammar[Expression::Unary::Postfix]
        expression ( call | access )*;
        '''
        while self.matches(*UNARY_POSTFIX_OPERATORS):
            match self.current.type:
                case Token.Type.SymbolLParen:
                    head = self._parse_expression_call(head)
                case Token.Type.SymbolDot:
                    head = self._parse_expression_access(head)
        return head

    def _parse_expression_call(self, head: UnresolvedNode) -> UnresolvedNode:
        '''
        Grammar[Expression::Call]
        '(' ( expression ( ',' expression )* )? ')';
        '''
        token = self.require(Token.Type.SymbolLParen)
        arguments: list[UnresolvedNode] = []
        # -Arguments: Zero
        if not self.consume(Token.Type.SymbolRParen):
            # -Arguments: One
            arguments.append(self._parse_expression())
            # -Arguments: Multi
            while self.consume(Token.Type.SymbolComma):
                arguments.append(self._parse_expression())
            _ = self.require(Token.Type.SymbolRParen)
        return UnresolvedUnaryPostfixNode(
            token.location, head,
            UnresolvedUnaryPostfixNode.Kind.Call,
            arguments
        )

    def _parse_expression_access(self, head: UnresolvedNode) -> UnresolvedNode:
        '''
        Grammar[Expression::Access]
        '.' ( '*' | IDENTIFIER );
        '''
        token = self.require(Token.Type.SymbolDot)
        # -Dereference
        if self.consume(Token.Type.SymbolStar):
            return UnresolvedUnaryPrefixNode(
                token.location,
                UnresolvedUnaryPrefixNode.Operator.Dereference,
                head
            )
        assert False, "TODO: Member access"

    def _parse_expression_primary(self) -> UnresolvedNode:
        '''
        Grammar[Expression::Primary]
        expression_group | expression_literal;
        '''
        node: UnresolvedNode
        if self.matches(Token.Type.SymbolLParen):
            node = self._parse_expression_group()
        else:
            node = self._parse_expression_literal()
        return self._parse_expression_unary_postfix(node)

    def _parse_expression_group(self) -> UnresolvedNode:
        '''
        Grammar[Expression::Group]
        '(' expression ')';
        '''
        token = self.require(Token.Type.SymbolLParen)
        node = self._parse_expression()
        _ = self.require(Token.Type.SymbolRParen)
        node = UnresolvedGroupNode(token.location, node)
        if self.matches(*EXPRESSION_STARTERS):
            node._target = self._parse_expression_unary_prefix()
        return node

    def _parse_expression_literal(self) -> UnresolvedNode:
        '''
        Grammar[Expression::Literal]
        TYPE | IDENTIFIER | BOOLEAN | INTEGER;
        '''
        # -Types
        if self.matches(*TYPES.keys()):
            token = self.next()
            _type = TYPES[token.type]
            return UnresolvedTypeNode(token.location, _type)
        # -Identifier
        elif self.consume(Token.Type.Identifier):
            return UnresolvedIdentifierNode(
                self._last_token.location,
                self._last_token.value_as(str)
            )
        # -Literals
        kind: UnresolvedLiteralNode.Kind
        value: AST_LITERAL_TYPES
        token = self.requires(*LITERALS)
        match token.type:
            case Token.Type.Integer:
                kind = UnresolvedLiteralNode.Kind.Integer
                value = token.value_as(int)
            case Token.Type.Boolean:
                kind = UnresolvedLiteralNode.Kind.Boolean
                value = token.value_as(bool)
            case _:
                assert False, "TODO: Error handling"
        return UnresolvedLiteralNode(token.location, kind, value)

    # -Instance Methods: Helpers
    def _try_parse_type(self) -> tuple[bool, UnresolvedNode]:
        '''Tries parsing a type unary prefix and returns if variable declaration'''
        is_decl = self.matches(*UNARY_PREFIX_MODIFIERS.keys())
        head = self._parse_expression_unary_prefix()
        if not is_decl:
            is_decl = self.matches(Token.Type.Identifier)
        return (is_decl, head)

    # -Class Methods
    @classmethod
    def from_lexer(cls, lexer: Lexer) -> Parser:
        '''Create a Parser instance from a given Lexer stream'''
        parser = cls(lexer.lex())
        parser.file = lexer.file
        return parser
