##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Expr Node: Literals           ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self
from .node import ExprNode

if TYPE_CHECKING:
    from . import ExprNodeVisitor
    from ....middleware import Symbol


## Classes
@dataclass(slots=True)
class ExprIntegerNode(ExprNode):
    """
    Resolved Integer Literal Expression
    Represents a literal integer value terminal.
    """
    # -Instance Methods
    def accept[T](self, visitor: ExprNodeVisitor[T]) -> T:
        return visitor.visit_integer(self)

    # -Properties
    value: int


@dataclass(slots=True)
class ExprVariableNode(ExprNode):
    """
    Resolved Variable Expression
    Represents an identifier value terminal.
    """
    # -Instance Methods
    def accept[T](self, visitor: ExprNodeVisitor[T]) -> T:
        return visitor.visit_variable(self)

    # -Class Methods
    @classmethod
    def from_symbol(cls, symbol: Symbol) -> Self:
        return cls(symbol.id, type=symbol.type)

    # -Properties
    id: int
