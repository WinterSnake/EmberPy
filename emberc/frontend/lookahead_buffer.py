##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Lookahead Buffer    ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Callable, Iterator
from typing import TypeVar, cast

## Constants
TItem = TypeVar('TItem')
TMatch = TypeVar('TMatch')
type TSelector[TItem, TMatch] = Callable[[TItem], TMatch] | None


## Functions
def _get_match_from_item(item: TItem, selector: TSelector[TItem, TMatch]) -> TMatch:
    """
    Returns TMatch either by casting TItem to TMatch
    or by calling the selector to get TMatch from TItem
    """
    if selector is not None:
        return selector(item)
    return cast(TMatch, item)


## Classes
class LookaheadBuffer[TItem, TMatch](ABC):
    """
    Lookahead(n) Base

    Defines an implementation for a lookahead(n) buffer
    Sub-classes must implement a _next() method
    """

    # -Constructor
    def __init__(
        self, iterator: Iterator[TItem],
        selector: TSelector[TItem, TMatch] = None
    ) -> None:
        self._source: Iterator[TItem] = iterator
        self._buffer: deque[TItem] = deque()
        self._selector: TSelector[TItem, TMatch] = selector

    # -Instance Methods
    def _next(self) -> TItem | None:
        '''Returns next TItem from source or None if end of iterator'''
        try:
            return next(self._source)
        except StopIteration:
            return None

    def _fill_buffer(self, count: int) -> None:
        '''Fills buffer with next N TItems from source'''
        for i in range(count):
            item = self._next()
            if item is None:
                break
            self._buffer.append(item)

    def advance(self) -> TItem | None:
        '''Returns TItem from buffer.left or next TItem from source'''
        if self._buffer:
            return self._buffer.popleft()
        return self._next()

    def peek(self, index: int = 0) -> TItem | None:
        '''Fills buffer to N TItem then returns buffer[N]'''
        if index < 0:
            raise IndexError(f"Tried to peek a negative amount ({index})")
        buffer_count = len(self._buffer)
        if buffer_count <= index:
            self._fill_buffer(index - buffer_count + 1)
        if len(self._buffer) <= index:
            return None
        return self._buffer[index]

    def consume(self, expected: TMatch) -> bool:
        '''Returns boolean of next TItem is TMatch'''
        value = self.peek()
        if value is None:
            return False
        match: TMatch = _get_match_from_item(value, self._selector)
        if match != expected:
            return False
        self.advance()
        return True

    def matches(self, *expected: TMatch) -> TItem | None:
        '''Returns TItem if in TMatches else None; does not consume'''
        value = self.peek()
        if value is None:
            return None
        match: TMatch = _get_match_from_item(value, self._selector)
        if match not in expected:
            return None
        return value
