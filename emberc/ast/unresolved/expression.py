##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Expression   ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from .node import UnresolvedNode


## Classes
@dataclass
class UnresolvedExprNode(UnresolvedNode):
    """
    Unresolved AST Node: Expression

    A container for a statement with an optional expression.
    """
    # -Properties
    _expression: UnresolvedNode | None

    @property
    def has_expression(self) -> bool:
        return self._expression is not None

    @property
    def expression(self) -> UnresolvedNode:
        assert self._expression is not None, "TODO: Error handling"
        return self._expression


@dataclass
class UnresolvedEmptyNode(UnresolvedNode):
    """
    Unresolved AST Node: Empty Expression

    A container for an empty/void expression.
    """
    pass
