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


## Functions
def _get_match_comparable(
    value: TItem, comparator: Callable[[TItem], TMatch] | None
) -> TMatch:
    """
    Returns TMatch either by casting TItem to TMatch
    or by calling the comparator to get TMatch from TItem
    """
    if comparator is not None:
        return comparator(value)
    return cast(TMatch, value)



## Classes
class LookaheadBuffer(ABC, Generic[TItem, TMatch]):
    """
    Lookahead(1) Base

    Defines an implementation for a lookahead(1) buffer
    Sub-classes must implement a _next() method
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
        '''Returns T in buffer or sets buffer to next T and returns buffered T'''
        if self._buffer is None:
            self._buffer = self._next()
        return self._buffer

    def _consume(self, match: TMatch) -> bool:
        '''Returns True if next T matches given match input else False'''
        value = self._peek()
        if value is None:
            return False
        comparable: TMatch = _get_match_comparable(value, self._comparator)
        if comparable != match:
            return False
        self._buffer = None
        return True

    def _match(self, *matches: TMatch) -> TItem | Literal[False]:
        '''Returns T if next T matches given match inputs else returns False'''
        value = self._peek()
        if value is None:
            return False
        comparable: TMatch = _get_match_comparable(value, self._comparator)
        if comparable not in matches:
            return False
        self._buffer = None
        return value


    # -Properties
    _buffer: TItem | None
    _comparator: Callable[[TItem], TMatch] | None
