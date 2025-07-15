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
from ..errors import EmberError
from ..location import Location
from ..middleware.nodes import (
    LITERAL,
    Node, NodeExpr,
    NodeDeclModule, NodeDeclFunction, NodeDeclVariable,
    NodeStmtBlock, NodeStmtCondition, NodeStmtLoop, NodeStmtExpression,
    NodeExprAssignment, NodeExprBinary, NodeExprUnary, NodeExprCall,
    NodeExprGroup, NodeExprVariable, NodeExprLiteral,
)
from ..middleware import Datatype, SymbolTable, get_datatype_from_token

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
UNARY_OPERATOR: dict[Token.Type, NodeExprUnary.Operator] = {
    Token.Type.SymbolMinus: NodeExprUnary.Operator.Minus,  # '-'
}
BINARY_OPERATOR: dict[Token.Type, tuple[NodeExprBinary.Operator, int]] = {
    # -Comparisons
    Token.Type.SymbolEqEq:   (NodeExprBinary.Operator.EqEq, 1),  # '=='
    Token.Type.SymbolBangEq: (NodeExprBinary.Operator.NtEq, 1),  # '!='
    Token.Type.SymbolLt:     (NodeExprBinary.Operator.Lt,   2),  # '<'
    Token.Type.SymbolGt:     (NodeExprBinary.Operator.Gt,   2),  # '>'
    Token.Type.SymbolLtEq:   (NodeExprBinary.Operator.LtEq, 2),  # '<='
    Token.Type.SymbolGtEq:   (NodeExprBinary.Operator.GtEq, 2),  # '>='
    # -Math
    Token.Type.SymbolPlus:    (NodeExprBinary.Operator.Add, 3),  # '+'
    Token.Type.SymbolMinus:   (NodeExprBinary.Operator.Sub, 3),  # '-'
    Token.Type.SymbolStar:    (NodeExprBinary.Operator.Mul, 4),  # '*'
    Token.Type.SymbolFSlash:  (NodeExprBinary.Operator.Div, 4),  # '/'
    Token.Type.SymbolPercent: (NodeExprBinary.Operator.Mod, 4),  # '%'
}


## Functions
def _parse_condition_expression(parser: Parser) -> NodeExpr | EmberError:
    """
    Helper function for parsing a condition expression between parenthesis

    [Grammar]
    '(' expression ')'
    """
    # --Invalid '(' consume
    if not parser._consume(Token.Type.SymbolLParen):
        return parser._error(EmberError.invalid_symbol, symbol='(')
    condition = parser._parse_expression()
    # --Invalid <expression> consume
    if isinstance(condition, EmberError):
        return condition
    # --Invalid ')' consume
    if not parser._consume(Token.Type.SymbolRParen):
        return parser._error(EmberError.invalid_symbol, symbol=')')
    return condition


def _get_type_or_error(parser: Parser) -> Token | EmberError:
    """Helper function for getting a typed token or returning error"""
    _type: Token | Literal[False]
    if not (_type := parser._match(*TYPES_TABLE)):
        if parser.is_at_end:
            return parser._error(EmberError.invalid_type_eof)
        else:
            assert not isinstance(_type, bool)
            return parser._error(
                EmberError.invalid_type, _type.location,
                value=get_token_repr(_type)
            )
    assert isinstance(_type, Token)
    return _type


def _get_identifier_or_error(parser: Parser) -> Token | EmberError:
    """Helper function for getting an identifier token or returning error"""
    _id: Token | None = parser._advance()
    # -Invalid {Identifier} consume (end of stream)
    if _id is None:
        return parser._error(EmberError.invalid_identifier_eof)
    # -Invalid {Identifier} consume
    elif _id.type is not Token.Type.Identifier:
        return parser._error(
            EmberError.invalid_identifier, value=get_token_repr(_id)
        )
    assert isinstance(_id, Token)
    return _id


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
        err = EmberError(code, location, **kwargs)
        self.errors.append(err)
        return err

    def _sync(self) -> None:
        while token := self._advance():
            # -Break on statement ';' boundry
            if token.type is Token.Type.SymbolSemicolon:
                # -Consume '}' if applicable
                _ = self._consume(Token.Type.SymbolRBrace)
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
        declaration_function | declaration_statement;
        '''
        # -Rule: Function Declaration
        if self._consume(Token.Type.KeywordFunction):
            return self._parse_declaration_function()
        # -Rule: Statement
        return self._parse_declaration_statement()

    def _parse_declaration_function(self) -> Node | EmberError:
        '''
        Grammar[Declaration::Function]
        'fn' IDENTIFIER '(' (parameter (',' parameter)*)? ')' ':' TYPE '{' declaration_statement* '}';
        '''
        # -Internal Functions
        def _parameter() -> int | EmberError:
            '''
            Grammar[Function::Parameter]
            TYPE IDENTIFIER;
            '''
            _type = _get_type_or_error(self)
            # --Invalid [Type] consume
            if isinstance(_type, EmberError):
                return _type
            _id = _get_identifier_or_error(self)
            # --Invalid {Identifier} consume
            if isinstance(_id, EmberError):
                return _id
            datatype = get_datatype_from_token(_type.type)
            return self._table.add(_id.value, datatype)

        # -Body
        _id = _get_identifier_or_error(self)
        # --Invalid {Identifier} consume
        if isinstance(_id, EmberError):
            return _id
        entry: int = self._table.add(_id.value, Datatype.Empty)
        # --Invalid '(' consume
        if not self._consume(Token.Type.SymbolLParen):
            return self._error(EmberError.invalid_symbol, symbol='(')
        parameters: list[int] | None = None
        # -Parameters 0
        if not self._consume(Token.Type.SymbolRParen):
            # -Parameters 1
            _param = _parameter()
            # --Invalid [Parameter] consume
            if isinstance(_param, EmberError):
                return _param
            parameters = [_param]
            # -Parameters 2+
            while self._consume(Token.Type.SymbolComma):
                _param = _parameter()
                # --Invalid [Parameter] consume
                if isinstance(_param, EmberError):
                    return _param
                parameters.append(_param)
            # --Invalid ')' consume
            if not self._consume(Token.Type.SymbolRParen):
                return self._error(EmberError.invalid_symbol, symbol=')')
        # --Invalid ':' consume
        if not self._consume(Token.Type.SymbolColon):
            return self._error(EmberError.invalid_symbol, symbol=':')
        _type = _get_type_or_error(self)
        # --Invalid [Type] consume
        if isinstance(_type, EmberError):
            return _type
        datatype = get_datatype_from_token(_type.type)
        self._table.lookup(entry).type = datatype
        # --Invalid '{' consume
        if not self._consume(Token.Type.SymbolLBrace):
            return self._error(EmberError.invalid_symbol, symbol='{')
        body = self._parse_statement_block()
        return NodeDeclFunction(entry, parameters, body)

    def _parse_declaration_statement(self) -> Node | EmberError:
        '''
        Grammar[Declaration::Statement]
        declaration_variable | statement;
        '''
        # -Rule: Variable Declaration
        if token := self._match(*TYPES_TABLE):
            return self._parse_declaration_variable(token)
        # -Rule: Statement
        return self._parse_statement()

    def _parse_declaration_variable(self, _type: Token) -> Node | EmberError:
        '''
        Grammar[Declaration::Variable]
        TYPE IDENTIFIER ('=' expression)? ';';
        '''
        _id = _get_identifier_or_error(self)
        # -Invalid {Identifier} consume
        if isinstance(_id, EmberError):
            return _id
        datatype = get_datatype_from_token(_type.type)
        entry: int = self._table.add(_id.value, datatype)
        initializer: NodeExpr | None = None
        if self._consume(Token.Type.SymbolEq):
            _initializer = self._parse_expression()
            # --Invalid <expression> consume
            if isinstance(_initializer, EmberError):
                return _initializer
            initializer = _initializer
        # --Invalid ';' consume
        if not self._consume(Token.Type.SymbolSemicolon):
            _ = self._error(EmberError.invalid_symbol, symbol=';')
        return NodeDeclVariable(entry, initializer)

    def _parse_statement(self) -> Node | EmberError:
        '''
        Grammar[Statement]
        statement_block | statement_conditional | statement_loop_do | statement_loop_for | statement_loop_while | statement_expression;
        '''
        # -Rule: Block
        if self._consume(Token.Type.SymbolLBrace):
            body = self._parse_statement_block()
            return NodeStmtBlock(body)
        # -Rule: Condition
        elif self._consume(Token.Type.KeywordIf):
            return self._parse_statement_condition()
        # -Rule: Loop :: Do
        elif self._consume(Token.Type.KeywordDo):
            return self._parse_statement_loop_do()
        # -Rule: Loop :: For
        elif self._consume(Token.Type.KeywordFor):
            return self._parse_statement_loop_for()
        # -Rule: Loop :: While
        elif self._consume(Token.Type.KeywordWhile):
            return self._parse_statement_loop_while()
        # -Rule: Expression
        return self._parse_statement_expression()

    def _parse_statement_block(self) -> Sequence[Node]:
        '''
        Grammar[Statement::Block]
        '{' declaration_statement* '}';
        '''
        nodes: list[Node] = []
        while not self._consume(Token.Type.SymbolRBrace):
            # --Invalid '}' consume
            if self.is_at_end:
                _ = self._error(EmberError.invalid_symbol, symbol='}')
                break
            node = self._parse_declaration_statement()
            # -Error Recovery
            if isinstance(node, EmberError):
                self._sync()
            else:
                nodes.append(node)
        return nodes

    def _parse_statement_condition(self) -> Node | EmberError:
        '''
        Grammar[Statement::Condition]
        'if' '(' expression ')' statement ('else' statement)?
        '''
        condition = _parse_condition_expression(self)
        # --Invalid <expression> consume
        if isinstance(condition, EmberError):
            return condition
        body = self._parse_statement()
        # --Invalid <statement> consume
        if isinstance(body, EmberError):
            return body
        branch: Node | None = None
        if self._consume(Token.Type.KeywordElse):
            _branch = self._parse_statement()
            # --Invalid <statement> consume
            if isinstance(_branch, EmberError):
                return _branch
            branch = _branch
        return NodeStmtCondition(condition, body, branch)

    def _parse_statement_loop_do(self) -> Node | EmberError:
        '''
        Grammar[Statement::Loop::Do]
        'do' statement 'while' '(' expression ')' ';';
        '''
        body = self._parse_statement()
        # --Invalid <statement> consume
        if isinstance(body, EmberError):
            return body
        # --Invalid 'while' consume
        if not self._consume(Token.Type.KeywordWhile):
            return self._error(EmberError.invalid_keyword, word='while')
        condition = _parse_condition_expression(self)
        # --Invalid <expression> consume
        if isinstance(condition, EmberError):
            return condition
        # --Invalid ';' consume
        if not self._consume(Token.Type.SymbolSemicolon):
            _ = self._error(EmberError.invalid_symbol, symbol=';')
        # --Desugar
        loop = NodeStmtLoop(condition, body)
        return NodeStmtBlock([body, loop])

    def _parse_statement_loop_for(self) -> Node | EmberError:
        '''
        Grammar[Statement::Loop::For]
        'for' '(' (declaration_variable | statement_expression)? ';' expression? ';' expression? ')' statement;
        '''
        # --Invalid '(' consume
        if not self._consume(Token.Type.SymbolLParen):
            return self._error(EmberError.invalid_symbol, symbol='(')
        # -<Initializer>-
        initializer: Node | None = None
        if not self._consume(Token.Type.SymbolSemicolon):
            # -Rule: Variable Declaration
            if token := self._match(*TYPES_TABLE):
                _initializer = self._parse_declaration_variable(token)
            # -Rule: Expression Statement
            else:
                _initializer = self._parse_statement_expression()
            # --Invalid <initializer> consume
            if isinstance(_initializer, EmberError):
                return _initializer
            initializer = _initializer
        # -<Condition>-
        condition: NodeExpr
        # --Expression
        if not self._consume(Token.Type.SymbolSemicolon):
            _condition = self._parse_expression()
            # --Invalid <expression> consume
            if isinstance(_condition, EmberError):
                return _condition
            condition = _condition
            # --Invalid ';' consume
            if not self._consume(Token.Type.SymbolSemicolon):
                return self._error(EmberError.invalid_symbol, symbol=';')
        # --Literal
        else:
            location = self._last_token.location
            condition = NodeExprLiteral(
                location, NodeExprLiteral.Type.Boolean, True
            )
        # -<Increment>-
        increment: NodeExpr | None = None
        if not self._consume(Token.Type.SymbolRParen):
            _increment = self._parse_expression()
            # --Invalid <expression> consume
            if isinstance(_increment, EmberError):
                return _increment
            # --Valid <expression>
            increment = _increment
            # --Invalid ')' consume
            if not self._consume(Token.Type.SymbolRParen):
                return self._error(EmberError.invalid_symbol, symbol=')')
        body = self._parse_statement()
        # --Invalid <statement> consume
        if isinstance(body, EmberError):
            return body
        # --Desugar
        if increment is not None:
            body = NodeStmtBlock([body, increment])
        body = NodeStmtLoop(condition, body)
        if initializer is not None:
            body = NodeStmtBlock([initializer, body])
        return body

    def _parse_statement_loop_while(self) -> Node | EmberError:
        '''
        Grammar[Statement::Loop::While]
        'while' '(' expression ')' statement;
        '''
        condition = _parse_condition_expression(self)
        # --Invalid <expression> consume
        if isinstance(condition, EmberError):
            return condition
        body = self._parse_statement()
        # --Invalid <statement> consume
        if isinstance(body, EmberError):
            return body
        return NodeStmtLoop(condition, body)

    def _parse_statement_expression(self) -> Node | EmberError:
        '''
        Grammar[Statement::Expression]
        expression ';';
        '''
        node = self._parse_expression()
        # --Invalid <expression> consume
        if isinstance(node, EmberError):
            return node
        # --Invalid ';' consume
        if not self._consume(Token.Type.SymbolSemicolon):
            _ = self._error(EmberError.invalid_symbol, symbol=';')
        return NodeStmtExpression(node)

    def _parse_expression(self) -> NodeExpr | EmberError:
        '''
        Grammar[Expression]
        expression_binary ('=' expression)?;
        '''
        l_value = self._parse_expression_binary()
        # --Invalid <expression> consume
        if isinstance(l_value, EmberError):
            return l_value
        if self._consume(Token.Type.SymbolEq):
            location = self._last_token.location
            r_value = self._parse_expression()
            # --Invalid <expression> consume
            if isinstance(r_value, EmberError):
                return r_value
            l_value = NodeExprAssignment(location, l_value, r_value)
        return l_value

    def _parse_expression_binary(
        self, current_precedence: int = 0
    ) -> NodeExpr | EmberError:
        '''
        Grammar[Expression::Binary]
        expression_primary (BINARY_OPERATOR expression_binary)*;
        '''
        lhs = self._parse_expression_unary()
        # --Invalid <expression> consume
        if isinstance(lhs, EmberError):
            return lhs
        while token := self._match(*BINARY_OPERATOR.keys()):
            operator = BINARY_OPERATOR[token.type][0]
            precedence = BINARY_OPERATOR[token.type][1]
            if precedence <= current_precedence:
                self._buffer = token
                break
            rhs = self._parse_expression_binary(precedence)
            # --Invalid <expression> consume
            if isinstance(rhs, EmberError):
                return rhs
            lhs = NodeExprBinary(token.location, operator, lhs, rhs)
        return lhs

    def _parse_expression_unary(self) -> NodeExpr | EmberError:
        '''
        Grammar[Expression::Unary]
        UNARY_PREFIX_OPERATOR expression_unary | expression_primary unary_postfix;
        '''
        # -Internal Methods
        def _function_call() -> list[NodeExpr] | EmberError | None:
            '''
            Grammar[Unary::Postfix::Call]
            '(' (expression (',' expression)*)? ')';
            '''
            arguments: list[NodeExpr] | None = None
            # --Arguments: 0
            if not self._consume(Token.Type.SymbolRParen):
                # --Arguments: 1
                _arg = self._parse_expression()
                # --Invalid <expression> consume
                if isinstance(_arg, EmberError):
                    return _arg
                arguments = [_arg]
                # --Arguments: 2+
                while self._consume(Token.Type.SymbolComma):
                    _arg = self._parse_expression()
                    # --Invalid <expression> consume
                    if isinstance(_arg, EmberError):
                        return _arg
                    arguments.append(_arg)
                # --Invalid ')' consume
                if not self._consume(Token.Type.SymbolRParen):
                    return self._error(EmberError.invalid_symbol, symbol=')')
            return arguments

        # -Body
        # -<Prefix>-
        if token := self._match(*UNARY_OPERATOR.keys()):
            operator = UNARY_OPERATOR[token.type]
            expression = self._parse_expression_unary()
            # --Invalid <expression> consume
            if isinstance(expression, EmberError):
                return expression
            return NodeExprUnary(token.location, operator, expression)
        # -<Primary>-
        node = self._parse_expression_primary()
        # --Invalid <expression> consume
        if isinstance(node, EmberError):
            return node
        # -<Postfix>-
        # --Rule: Function Call
        while self._consume(Token.Type.SymbolLParen):
            arguments = _function_call()
            if isinstance(arguments, EmberError):
                return arguments
            node = NodeExprCall(node, arguments)
        return node

    def _parse_expression_primary(self) -> NodeExpr | EmberError:
        '''
        Grammar[Expression::Primary]
        IDENTIFIER | BOOLEAN | NUMBER | '(' expression ')';
        '''
        # -Rule: Group
        if self._consume(Token.Type.SymbolLParen):
            node = self._parse_expression()
            # --Invalid <expression> consume
            if isinstance(node, EmberError):
                return node
            # -Invalid ')' consume
            if not self._consume(Token.Type.SymbolRParen):
                _ = self._error(EmberError.invalid_symbol, symbol=')')
            return NodeExprGroup(node)
        # -Rule: Literal
        _type: NodeExprLiteral.Type
        value: LITERAL
        literal = self._advance()
        # -Invalid <expression> consume (end of stream)
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
            # -Invalid <expression> consume
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
