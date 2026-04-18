##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Diagnostics: Engine           ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from ..core import Location


## Classes
@dataclass(frozen=True, slots=True)
class Diagnostic:
    """
    A finalized snapshot of a compilation event, containing 
    metadata regarding the severity, the specific error code, 
    and the physical span within the source code.
    """
    # -Properties
    level: Diagnostic.Level
    code: Diagnostic.Code
    message: str
    start: Location
    _end: Location | None

    def has_end(self) -> bool:
        return self._end is not None

    def end(self) -> Location:
        if self._end is None:
            raise ValueError(f"Tried getting end location from non-end holding diagnostic")
        return self._end

    # -Sub-Classes
    class Level(IntEnum):
        Trace = 0
        Info = 100
        Warn = 200
        Error = 300
        Fatal = 400

    class Code(Enum):
        # -Lexer :: Info
        # -Lexer :: Warn
        # -Lexer :: Error
        LE001 = "Invalid character '{0}' found"

        # -Instance Methods
        def format(self, *args: Any) -> str:
            return self.value.format(*args)
