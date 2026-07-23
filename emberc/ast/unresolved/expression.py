##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Expression   ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from . import UnresolvedNodeVisitor


## Classes
@dataclass(slots=True)
class UnresolvedExpressionNode(UnresolvedNode):
    """Expression Statement AST node."""
    # -Instance Methods
    def accept[R](self, visitor: UnresolvedNodeVisitor[R]) -> R:
        return visitor.visit_expression(self)

    # -Properties
    expression: UnresolvedNode


@dataclass(slots=True)
class UnresolvedGroupNode(UnresolvedNode):
    """Group Expression AST node with inner wrapped expression."""
    # -Instance Methods
    def accept[R](self, visitor: UnresolvedNodeVisitor[R]) -> R:
        return visitor.visit_group(self)

    # -Properties
    inner: UnresolvedNode
