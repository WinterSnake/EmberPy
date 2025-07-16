##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Parser                        ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Callable, Sequence
from typing import Any, Iterator, Literal
from .lookahead_buffer import LookaheadBuffer
from .token import Token, get_token_repr
from ..errors import EmberError
from ..location import Location
from ..middleware.nodes import (
    LITERAL,
    Node, NodeExpr,
    NodeDeclModule, NodeDeclFunction, NodeDeclVariable,
    NodeStmtBlock, NodeStmtCondition, NodeStmtLoop, NodeStmtReturn,
    NodeStmtExpression,
    NodeExprAssignment, NodeExprBinary, NodeExprUnary, NodeExprCall,
    NodeExprGroup, NodeExprVariable, NodeExprLiteral,
)
from ..middleware import Datatype, get_datatype_from_token

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
    Token.Type.SymbolBang: NodeExprUnary.Operator.Negate,  # '!'
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


def _try_get_type(parser: Parser) -> Token | Literal[False]:
    """Helper function for trying to parse a typed token"""
    token: Token | Literal[False]
    if not (token := parser._match(*TYPES_TABLE)):
        return False
    assert isinstance(token, Token)
    return token


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
    def parse(self) -> Node:
        '''
        Grammar[Module]
        declaration*;
        '''
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
        def _parameter() -> NodeDeclFunction.Parameter | EmberError:
            '''
            Grammar[Declaration::Function::Parameter]
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
            datatype = get_datatype_from_token(_type)
            return NodeDeclFunction.Parameter(_id.value, datatype)

        # -Body
        _id = _get_identifier_or_error(self)
        # --Invalid {Identifier} consume
        if isinstance(_id, EmberError):
            return _id
        # --Invalid '(' consume
        if not self._consume(Token.Type.SymbolLParen):
            return self._error(EmberError.invalid_symbol, symbol='(')
        parameters: list[NodeDeclFunction.Parameter] = []
        # -Parameters: 0
        if not self._consume(Token.Type.SymbolRParen):
            # -Parameters: 1
            _param = _parameter()
            # --Invalid [Parameter] consume
            if isinstance(_param, EmberError):
                return _param
            parameters = [_param]
            # -Parameter: 2+
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
        return_type = get_datatype_from_token(_type)
        # --Invalid '{' consume
        if not self._consume(Token.Type.SymbolLBrace):
            return self._error(EmberError.invalid_symbol, symbol='{')
        body = self._parse_statement_block()
        return NodeDeclFunction(_id.value, parameters, return_type, body)

    def _parse_declaration_statement(self) -> Node | EmberError:
        '''
        Grammar[Declaration::Statement]
        declaration_variable | statement;
        '''
        # -Rule: Variable Declaration
        if token := _try_get_type(self):
            return self._parse_declaration_variable(token)
        # -Rule: Statement
        return self._parse_statement()

    def _parse_declaration_variable(self, _type: Token) -> Node | EmberError:
        '''
        Grammar[Declaration::Variable]
        TYPE variable (',' variable)* ';';
        '''
        # -Internal Functions
        def _variable() -> NodeDeclVariable.Variable | EmberError:
            '''
            Grammar[Declaration::Variable::Variable]
            IDENTIFIER ('=' expression)?;
            '''
            _id = _get_identifier_or_error(self)
            # -Invalid {Identifier} consume
            if isinstance(_id, EmberError):
                return _id
            initializer: NodeExpr | None = None
            if self._consume(Token.Type.SymbolEq):
                _initializer = self._parse_expression()
                # --Invalid <expression> consume
                if isinstance(_initializer, EmberError):
                    return _initializer
                initializer = _initializer
            return NodeDeclVariable.Variable(_id.value, initializer)

        # -Body
        datatype = get_datatype_from_token(_type)
        _var = _variable()
        if isinstance(_var, EmberError):
            return _var
        variables: list[NodeDeclVariable.Variable] = [_var]
        while self._consume(Token.Type.SymbolComma):
            _var = _variable()
            if isinstance(_var, EmberError):
                return _var
            variables.append(_var)
        # --Invalid ';' consume
        if not self._consume(Token.Type.SymbolSemicolon):
            _ = self._error(EmberError.invalid_symbol, symbol=';')
        return NodeDeclVariable(datatype, variables)

    def _parse_statement(self) -> Node | EmberError:
        '''
        Grammar[Statement]
        statement_block | statement_conditional
        | statement_loop_do | statement_loop_for | statement_loop_while
        | statement_return | statement_expression;
        '''
        type RuleEntry = Callable[[], Node | EmberError]
        rule_table: dict[Token.Type, RuleEntry] = {
            Token.Type.SymbolLBrace:
                lambda: NodeStmtBlock(self._parse_statement_block()),
            Token.Type.KeywordIf: self._parse_statement_condition,
            Token.Type.KeywordDo: self._parse_statement_loop_do,
            Token.Type.KeywordWhile: self._parse_statement_loop_while,
            Token.Type.KeywordFor: self._parse_statement_loop_for,
            Token.Type.KeywordReturn: self._parse_statement_return,
        }
        if rule := self._match(*rule_table.keys()):
            return rule_table[rule.type]()
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
        elif not self._consume(Token.Type.KeywordWhile):
            return self._error(EmberError.invalid_keyword, word='while')
        condition = _parse_condition_expression(self)
        # --Invalid <expression> consume
        if isinstance(condition, EmberError):
            return condition
        # --Invalid ';' consume
        elif not self._consume(Token.Type.SymbolSemicolon):
            _ = self._error(EmberError.invalid_symbol, symbol=';')
        # --Desugar
        return NodeStmtBlock([body, NodeStmtLoop(condition, body)])

    def _parse_statement_loop_for(self) -> Node | EmberError:
        '''
        Grammar[Statement::Loop::For]
        'for' '(' (declaration_variable | statement_expression | ';') expression? ';' expression? ')' statement;
        '''
        # --Invalid '(' consume
        if not self._consume(Token.Type.SymbolLParen):
            return self._error(EmberError.invalid_symbol, symbol='(')
        # -<Initializer>-
        initializer: Node | None = None
        if not self._consume(Token.Type.SymbolSemicolon):
            # -Rule: Variable Declaration
            if token := _try_get_type(self):
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
            # --Invalid ';' consume
            elif not self._consume(Token.Type.SymbolSemicolon):
                return self._error(EmberError.invalid_symbol, symbol=';')
            condition = _condition
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
            # --Invalid ')' consume
            elif not self._consume(Token.Type.SymbolRParen):
                return self._error(EmberError.invalid_symbol, symbol=')')
            increment = _increment
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

    def _parse_statement_return(self) -> Node | EmberError:
        '''
        Grammar[Statement::Return]
        'return' expression? ';';
        '''
        node: NodeExpr | None = None
        if not self._consume(Token.Type.SymbolSemicolon):
            _node = self._parse_expression()
            # --Invalid <expression> consume
            if isinstance(_node, EmberError):
                return _node
            # --Invalid ';' consume
            elif not self._consume(Token.Type.SymbolSemicolon):
                _ = self._error(EmberError.invalid_symbol, symbol=';')
            node = _node
        return NodeStmtReturn(node)

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

    def _parse_expression_binary(self, precedence: int = 0) -> NodeExpr | EmberError:
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
            _precedence = BINARY_OPERATOR[token.type][1]
            if _precedence <= precedence:
                self._buffer = token
                break
            rhs = self._parse_expression_binary(_precedence)
            # --Invalid <expression> consume
            if isinstance(rhs, EmberError):
                return rhs
            lhs = NodeExprBinary(token.location, operator, lhs, rhs)
        return lhs

    def _parse_expression_unary(self) -> NodeExpr | EmberError:
        '''
        Grammar[Expression::Unary]
        UNARY_PREFIX_OPERATOR expression_unary | expression_call;
        '''
        if token := self._match(*UNARY_OPERATOR.keys()):
            operator = UNARY_OPERATOR[token.type]
            expression = self._parse_expression_unary()
            # --Invalid <expression> consume
            if isinstance(expression, EmberError):
                return expression
            return NodeExprUnary(token.location, operator, expression)
        return self._parse_expression_call()

    def _parse_expression_call(self) -> NodeExpr | EmberError:
        '''
        Grammar[Expression::Call]
        expression_primary function_call*;
        '''
        # -Internal Methods
        def _function_call() -> list[NodeExpr] | EmberError:
            '''
            Grammar[Unary::Postfix::Call]
            '(' (expression (',' expression)*)? ')';
            '''
            arguments: list[NodeExpr] = []
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
        node = self._parse_expression_primary()
        if isinstance(node, EmberError):
            return node
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
            elif not self._consume(Token.Type.SymbolRParen):
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
                return NodeExprVariable(literal.location, literal.value)
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
