##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Diagnostics: Diagnostic       ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from enum import Enum, IntEnum, auto
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence
    from ..core import Span


## Classes
@dataclass(frozen=False, init=False, slots=True)
class Diagnostic:
    """Compiler engine report bound to a location, code, and context."""
    # -Constructor
    def __init__(
        self, level: Diagnostic.Level, code: Diagnostic.Code,
        location: Span, *args: Any
    ) -> None:
        self.level = level
        self.code = code
        self.location = location
        self.args = args

    # -Properties
    level: Diagnostic.Level
    code: Diagnostic.Code
    location: Span
    args: Sequence[Any]

    @property
    def name(self) -> str:
        '''Return diagnostic code.'''
        return self.code.name

    @property
    def message(self) -> str:
        '''Return diagnostic message.'''
        return self.code.value[0]

    @property
    def is_formatted(self) -> bool:
        '''Return if diagnostic message needs formatting.'''
        return self.code.value[1]

    # -Sub-Classes
    class Code(Enum):
        # -Lexer
        E1001 = ("Unknown character '{0}' found", True)
        E1002 = ("Unterminated multi-line comment; expected '*/'", False)
        # -Parser
        E2001 = ("Identifier expected", False)
        E2002 = ("Expression expected", False)
        E2003 = ("Condition expression must be enclosed in parentheses", False)
        E2101 = ("';' expected", False)
        E2102 = ("')' expected", False)
        E2103 = ("'}' expected", False)

    class Level(IntEnum):
        Error = auto()
        Warn = auto()
