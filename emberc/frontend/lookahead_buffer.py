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
type TKey[TItem, TMatch] = Callable[[TItem], TMatch] | None


## Functions
def _get_match_key(item: TItem, key: TKey[TItem, TMatch]) -> TMatch:
    """
    Returns TMatch either by casting TItem to TMatch
    or by calling the key to get TMatch from TItem
    """
    if key is not None:
        return key(item)
    return cast(TMatch, item)


## Classes
class LookaheadBuffer[TItem, TMatch](ABC):
    """
    Lookahead(1) Base

    Defines an implementation for a lookahead(1) buffer
    Sub-classes must implement a _next() method
    """

    # -Instance Methods
    @abstractmethod
    def _next(self) -> TItem | None: ...

    def _advance(self) -> TItem | None:
        '''Returns TItem in buffer and resets buffer or returns next TItem'''
        if self._buffer:
            value = self._buffer
            self._buffer = None
            return value
        return self._next()

    def _peek(self) -> TItem | None:
        '''Returns TItem in buffer or sets buffer to next TItem and returns buffered TItem'''
        if self._buffer is None:
            self._buffer = self._next()
        return self._buffer

    def _consume(self, match: TMatch) -> bool:
        '''Returns True if next TItem key is TMatch else False and sets buffer'''
        value = self._peek()
        if value is None:
            return False
        key: TMatch = _get_match_key(value, self._key)
        if key != match:
            return False
        self._buffer = None
        return True

    def _match(self, *matches: TMatch) -> TItem | Literal[False]:
        '''Returns TItem if next TItem key is in matches else returns False and sets buffer'''
        value = self._peek()
        if value is None:
            return False
        key: TMatch = _get_match_key(value, self._key)
        if key not in matches:
            return False
        self._buffer = None
        return value


    # -Properties
    _buffer: TItem | None = None
    _key: TKey[TItem, TMatch] = None
