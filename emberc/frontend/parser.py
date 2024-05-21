#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Lexer               ##
##-------------------------------##

## Imports
from .token import Token
from .node import Node

## Constants
__all__: tuple[str] = ("parse",)


## Functions
def _consume_token(tokens: list[Token], _type: Token.Type) -> Token | None:
    """"""
    if tokens[0].type != _type:
        return None
    return tokens.pop(0)


def _match_token(tokens: list[Token], _type: Token.Type) -> bool:
    """"""
    if tokens[0].type != _type:
        return False
    tokens.pop(0)
    return True


def parse(tokens: list[Token]) -> Node | None:
    """"""
    if _match_token(tokens, Token.Type.KeywordFunction):
        ident = _consume_token(tokens, Token.Type.Identifier)
        if ident is None:
            return None
        for expected_token in (
            Token.Type.SymbolLParen, Token.Type.SymbolRParen,
            Token.Type.SymbolLBracket, Token.Type.SymbolRBracket
        ):
            _t = _consume_token(tokens, expected_token)
            if _t is None:
                return None
        return Node(ident.value)
    return None
