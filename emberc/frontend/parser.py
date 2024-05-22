#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Lexer               ##
##-------------------------------##

## Imports
from .token import Token
from .node import (
    Node, NodeDefinition, NodeAssignment, NodeBinExpr, NodeLiteral
)

## Constants
__all__: tuple[str] = ("parse",)
MAPPEDOPERATORS: dict[Token.Type, NodeBinExpr.Type] = {
    Token.Type.SymbolPlus: NodeBinExpr.Type.Add,
    Token.Type.SymbolMinus: NodeBinExpr.Type.Sub,
    Token.Type.SymbolAsterisk: NodeBinExpr.Type.Mul,
    Token.Type.SymbolSlash: NodeBinExpr.Type.Div,
    Token.Type.SymbolPercent: NodeBinExpr.Type.Mod,
}


## Functions
def _consume_token(tokens: list[Token], _type: Token.Type) -> Token | None:
    """"""
    if not tokens or tokens[0].type != _type:
        return None
    return tokens.pop(0)


def _check_token(tokens: list[Token], *_types: Token.Type) -> bool:
    """"""
    for _type in _types:
        if tokens[0].type == _type:
            return True
    return False


def parse(tokens: list[Token]) -> list[Node] | None:
    """"""
    nodes: list[Node] = []
    while tokens:
        node = _parse_statement(tokens)
        if node is None:
            return None
        nodes.append(node)
    return nodes


def _parse_statement(tokens: list[Token]) -> Node | None:
    """"""
    node: Node | None
    # -Definition
    if _check_token(tokens, Token.Type.TypeInt32):
        _type = tokens.pop(0)
        name = _consume_token(tokens, Token.Type.Identifier)
        if name is None or _consume_token(tokens, Token.Type.SymbolEqual) is None:
            return None
        value = _parse_expr(tokens)
        if value is None:
            return None
        assert(isinstance(name.value, str))
        node = NodeDefinition(None, name.value, value)
    # -BinExpr
    else:
        node = _parse_expr(tokens)
    if _consume_token(tokens, Token.Type.SymbolSemicolon) is None:
        return None
    return node


def _parse_expr(tokens: list[Token]) -> Node | None:
    """"""
    return _parse_binexpr_term(tokens)


def _parse_binexpr_term(tokens: list[Token]) -> Node | None:
    """"""
    node = _parse_binexpr_factor(tokens)
    if node is None:
        return None
    while _check_token(tokens, Token.Type.SymbolPlus, Token.Type.SymbolMinus):
        operator = MAPPEDOPERATORS.get(tokens.pop(0).type)
        assert(operator is not None)
        rhs = _parse_binexpr_factor(tokens)
        if rhs is None:
            return None
        node = NodeBinExpr(operator, node, rhs)
    return node


def _parse_binexpr_factor(tokens: list[Token]) -> Node | None:
    """"""
    node = _parse_primary(tokens)
    if node is None:
        return None
    while _check_token(
        tokens, Token.Type.SymbolAsterisk, Token.Type.SymbolSlash, Token.Type.SymbolPercent
    ):
        operator = MAPPEDOPERATORS.get(tokens.pop(0).type)
        assert(operator is not None)
        rhs = _parse_primary(tokens)
        if rhs is None:
            return None
        node = NodeBinExpr(operator, node, rhs)
    return node


def _parse_primary(tokens: list[Token]) -> Node | None:
    """"""
    if _consume_token(tokens, Token.Type.SymbolLParen):
        node = _parse_expr(tokens)
        if _consume_token(tokens, Token.Type.SymbolRParen) is None:
            return None
        return node
    return _parse_literal(tokens)


def _parse_literal(tokens: list[Token]) -> Node | None:
    """"""
    token = tokens.pop(0)
    if token is None:
        return None
    # -Assignment
    if _consume_token(tokens, Token.Type.SymbolEqual):
        value = _parse_expr(tokens)
        if value is None:
            return None
        assert(isinstance(token.value, str))
        return NodeAssignment(token.value, value)
    # -Literal
    assert(isinstance(token.value, str))
    match token.type:
        case Token.Type.Identifier:
            return NodeLiteral(NodeLiteral.Type.Identifier, token.value)
        case Token.Type.Integer:
            return NodeLiteral(NodeLiteral.Type.Integer, int(token.value))
    return None
    
