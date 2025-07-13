##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Lookahead Buffer              ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Generic, Literal, TypeVar, cast

## Constants
TItem = TypeVar('TItem')
TMatch = TypeVar('TMatch')


## Classes
class LookaheadBuffer(ABC, Generic[TItem, TMatch]):
    """
    Lookahead(1) Base

    Defines an implementation for lookahead(1)
    """

    # -Instance Methods
    @abstractmethod
    def _next(self) -> TItem | None: ...

    def _advance(self) -> TItem | None:
        '''Returns T in buffer and resets buffer or returns next T'''
        if self._buffer:
            value = self._buffer
            self._buffer = None
            return value
        return self._next()

    def _peek(self) -> TItem | None:
        '''Returns T in buffer or sets buffer to next T and returns T'''
        if self._buffer is None:
            self._buffer = self._next()
        return self._buffer

    def _match(self, *matches: TMatch) -> TItem | Literal[False]:
        '''Returns T if T matches given match inputs else returns False'''
        value = self._peek()
        if value is None:
            return False
        comparable: TMatch
        if self._comparison:
            comparable = self._comparison(value)
        else:
            comparable = cast(TMatch, value)
        if comparable not in matches:
            return False
        self._buffer = None
        return value


    # -Properties
    _buffer: TItem | None
    _comparison: Callable[[TItem], TMatch] | None
