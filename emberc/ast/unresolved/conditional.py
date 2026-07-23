##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Conditional  ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from . import UnresolvedNodeVisitor
    from ...core import Span


## Classes
@dataclass(slots=True)
class UnresolvedConditionalNode(UnresolvedNode):
    """Conditional AST node with condition and then/else branches."""
    # -Instance Methods
    def accept[R](self, visitor: UnresolvedNodeVisitor[R]) -> R:
        return visitor.visit_conditional(self)

    # -Properties
    condition: UnresolvedNode
    then_branch: UnresolvedNode
    _else_branch: UnresolvedNode | None

    @property
    def has_else_branch(self) -> bool:
        '''Return if conditional has else branch.'''
        return self._else_branch is not None

    @property
    def else_branch(self) -> UnresolvedNode:
        '''Return else branch node; assert node exists.'''
        assert self._else_branch is not None
        return self._else_branch
