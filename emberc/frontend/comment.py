##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Comment             ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from ..core import Span


## Classes
@dataclass(frozen=True, slots=True)
class Comment:
    """
    Source Comment

    Represents an inlined or multi-lined comment within source's text.
    """
    # -Properties
    span: Span
    _children: Sequence[Comment] | None

    @property
    def is_inline(self) -> bool:
        '''Return if comment is inlined.'''
        return self._children is None

    @property
    def children(self) -> Sequence[Comment]:
        '''Return children of multi-line comment.'''
        assert self._children is not None
        return self._children
