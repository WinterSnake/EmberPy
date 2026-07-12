##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Core: Span                    ##
##-------------------------------##

## Imports
from dataclasses import dataclass


## Classes
@dataclass(frozen=True, slots=True)
class Span:
    """
    Represents a continuous region of text within a specific source file.
    
    Used by the lexer, parser, and AST nodes to track precise byte/character 
    offsets for error reporting, syntax highlighting, and source-to-token mapping.
    """

    # -Dunder Methods
    def __len__(self) -> int:
        return self.end - self.start

    # -Instance Methods
    def start_at(self, position: int) -> Span:
        return Span(self.id, position, self.end)

    def end_at(self, position: int) -> Span:
        return Span(self.id, self.start, position)

    def extend_from(self, other: Span) -> Span:
        if self.id != other.id:
            raise ValueError("Cannot combine spans of different sources")
        return Span(self.id, other.start, self.end)

    def extend_to(self, other: Span) -> Span:
        if self.id != other.id:
            raise ValueError("Cannot combine spans of different sources")
        return Span(self.id, self.start, other.end)

    # -Properties
    id: int
    start: int
    end: int

    @property
    def offsets(self) -> tuple[int, int]:
        return (self.start, self.end)
