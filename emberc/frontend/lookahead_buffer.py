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
        self._source = iterator
        self._buffer = deque()
        self._selector = selector

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
        buffer_count = len(self._buffer)
        if buffer_count <= index:
            self._fill_buffer(index - buffer_count + 1)
        if len(self._buffer) <= index:
            return None
        return self._buffer[index]

    # -Properties
    _source: Iterator[TItem]
    _buffer: deque[TItem]
    _selector: TSelector[TItem, TMatch]
