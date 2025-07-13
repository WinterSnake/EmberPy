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
STEPS: tuple[str, ...] = ("Lexer", "Parser")
ERROR_TABLE: tuple[tuple[str, ...], ...] = (
    # -Lexer
    (
        "Unexpected character '{char}'",
        "Unknown symbol '{char}'",
        "Unterminated multiline comment",
    ),
    # -Parser
    (),
)

## Functions
def parse_debug_level(level: str) -> DebugLevel:
    match level:
        case "trace":
            return DebugLevel.Trace
        case "info":
            return DebugLevel.Info
        case _:
            return DebugLevel.Off


## Classes
class DebugLevel(IntEnum):
    Trace = auto()
    Info = auto()
    Off = auto()


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
        index: int = self.code // 1000 - 1
        step: str = STEPS[index]
        message: str = ERROR_TABLE[index][self.code % 1000 - 1]
        if self.kwargs:
            message = message.format(**self.kwargs)
        message = f"{step} Error {self.code} {message}"
        if self.location:
            message = f"[{self.location}] {message}"
        return message

    # -Class Properties
    # --Code: Lexer
    unexpected_character: ClassVar[int] = 1001
    unknown_symbol: ClassVar[int] = 1002
    unterminated_comment_multiline: ClassVar[int] = 1003
