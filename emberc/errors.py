##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Error                         ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any, ClassVar
from .location import Location

## Constants
PHASE: tuple[str, ...] = ("Lexical", "Syntax")
ERROR_TABLE: tuple[tuple[str, ...], ...] = (
    # -Lexer
    (
        "Unexpected character '{char}'",
        "Unknown symbol '{char}'",
        "Unterminated multiline comment",
    ),
    # -Parser
    (
        "'{symbol}' expected",
        "Invalid expression term '{value}'",
        "Expected expression",
        "Invalid identifier '{value}'",
        "Expected identifier",
        "Invalid type '{value}'",
        "Type expected",
    ),
)


## Classes
class EmberError:
    """
    Ember Compiler Error
    
    Uses a lookup table for the error code handling
    and formats the error message with appropriate details
    """

    # -Constructor
    def __init__(self, code: int, location: Location | None = None, **kwargs: Any) -> None:
        self.code: int = code
        self.location: Location | None = location
        self.kwargs: dict[str, Any] = kwargs

    # -Properties
    @property
    def message(self) -> str:
        offset: int = 100
        index: int = self.code // offset - 1
        phase: str = PHASE[index]
        message: str = ERROR_TABLE[index][self.code % offset - 1]
        if self.kwargs:
            message = message.format(**self.kwargs)
        message = f"{phase} error {self.code}: {message}"
        if self.location:
            message = f"[{self.location}] {message}"
        return message

    # -Class Properties
    # --Code: Lexer
    unexpected_character: ClassVar[int] = 101
    unknown_symbol: ClassVar[int] = 102
    unterminated_comment_multiline: ClassVar[int] = 103
    # --Code: Parser
    invalid_consume_symbol: ClassVar[int] = 201
    invalid_expression: ClassVar[int] = 202
    invalid_expression_eof: ClassVar[int] = 203
    invalid_identifier: ClassVar[int] = 204
    invalid_identifier_eof: ClassVar[int] = 205
    invalid_type: ClassVar[int] = 206
    invalid_type_eof: ClassVar[int] = 207
