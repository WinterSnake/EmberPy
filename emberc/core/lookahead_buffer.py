##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Core: Lookahead Buffer        ##
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
    Lookahead(n) Buffer

    A generic wrapper for iterators that provides arbitrary 
    lookahead and item matching without premature consumption.
    """

    # -Constructor
    def __init__(
        self, source: Iterator[TItem],
        selector: TSelector[TItem, TMatch] = None
    ) -> None:
        self._source: Iterator[TItem] = source
        self._selector: TSelector[TItem, TMatch] = selector
        self._buffer: deque[TItem] = deque()
        self.is_at_end: bool = False

    # -Instance Methods
    def advance(self) -> TItem | None:
        '''Returns next TItem from buffer or source iterator; None if at end'''
        if self.is_at_end:
            return None
        elif self._buffer:
            return self._buffer.popleft()
        item = next(self._source, None)
        if item is None:
            self.is_at_end = True
        return item

    def next(self) -> TItem:
        '''Returns next TItem; asserts TItem exists'''
        item = self.advance()
        assert item is not None
        return item

    def peek(self, index: int = 0) -> TItem | None:
        '''Fills buffer to N+1 TItem then returns buffer[N]; None if beyond source iterator'''
        if index < 0:
            raise IndexError(f"Tried to peek a negative amount ({index})")
        buffer_count = len(self._buffer)
        if buffer_count <= index:
            for _ in range(index - buffer_count + 1):
                item = next(self._source, None)
                if item is None:
                    break
                self._buffer.append(item)
                buffer_count += 1
        if buffer_count <= index:
            return None
        return self._buffer[index]

    def consume(self, expected: TMatch) -> bool:
        '''Returns boolean if next TItem is TMatch; consumes'''
        value = self.peek()
        if value is None:
            return False
        match: TMatch = _get_match_from_item(value, self._selector)
        if match != expected:
            return False
        _ = self.advance()
        return True

    def matches(self, *expected: TMatch) -> bool:
        '''Returns boolean if next TItem in TMatches; does not consume'''
        value = self.peek()
        if value is None:
            return False
        match: TMatch = _get_match_from_item(value, self._selector)
        if match not in expected:
            return False
        return True

    # -Properties
    @property
    def current(self) -> TItem:
        '''Returns current TItem from iterator; asserts TItem exists'''
        item = self.peek()
        assert item is not None
        return item
