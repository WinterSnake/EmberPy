#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Lexer               ##
##-------------------------------##

## Imports
from .token import Token
from .node import Node, NodeBinExpr, NodeLiteral

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
def _consume_token(tokens: list[Token], _type: Token.Type | None = None) -> Token | None:
    """"""
    if not tokens or (_type is not None and tokens[0].type != _type):
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
    node = _parse_expr(tokens)
    if _consume_token(tokens, Token.Type.SymbolSemiColon) is None:
        return None
    return node


def _parse_expr(tokens: list[Token]) -> NodeBinExpr | None:
    """"""
    lhs = _parse_primary(tokens)
    while _check_token(
        tokens, Token.Type.SymbolPlus, Token.Type.SymbolMinus,
        Token.Type.SymbolAsterisk, Token.Type.SymbolSlash, Token.Type.SymbolPercent
    ):
        operator = _consume_token(tokens)
        rhs = _parse_expr(tokens)
        if rhs is None:
            return None
        return NodeBinExpr(MAPPEDOPERATORS.get(operator.type), lhs, rhs)
    return lhs


def _parse_primary(tokens: list[Token]) -> Node | None:
    """"""
    if _consume_token(tokens, Token.Type.SymbolLParen):
        expr = _parse_expr(tokens)
        if _consume_token(tokens, Token.Type.SymbolRParen) is None:
            return None
        return expr
    return _parse_literal(tokens)


def _parse_literal(tokens: list[Token]) -> NodeLiteral | None:
    """"""
    token = _consume_token(tokens, Token.Type.Integer)
    if token is None:
        return None
    return NodeLiteral(NodeLiteral.Type.Integer, int(token.value))
