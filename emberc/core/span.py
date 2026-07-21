##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Core: Span                    ##
##-------------------------------##

## Imports
from dataclasses import dataclass, field, replace
from typing import Self


## Classes
@dataclass(frozen=True, slots=True)
class Span:
    """Contiguous slice of source text bound by start and end offsets."""
    # -Dunder Methods
    def __len__(self) -> int:
        return self.end - self.start

    # -Instance Methods
    def start_at(self, position: int) -> Span:
        '''Create a new span with the given start position.'''
        return replace(self, start=position)

    def end_at(self, position: int) -> Span:
        '''Create a new span with the given end position.'''
        return replace(self, end=position)

    def extend_from(self, span: Span) -> Span:
        '''Create a new span extended backward from the start of another span.'''
        assert self.id == span.id, "Cannot extend different source spans."
        return replace(self, start=span.start)

    def extend_to(self, span: Span) -> Span:
        '''Create a new span extended forward to the end of another span.'''
        assert self.id == span.id, "Cannot extend different source spans."
        return replace(self, end=span.end)

    # -Class Methods
    @classmethod
    def point(cls, _id: int, position: int) -> Self:
        return cls(_id, position, position + 1)

    # -Properties
    id: int = field(repr=False)
    start: int
    end: int
