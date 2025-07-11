##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression - Primary    ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any
from .core import NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeExprGroup(NodeExpr):
    """
    Ember Node: Expression :: Group
    Represents an AST node of a grouped expression
    """

    # -Constructor
    def __init__(self, location: Location, expression: NodeExpr) -> None:
        super().__init__(location)
        self.expression: NodeExpr = expression

    # -Dunder Methods
    def __str__(self) -> str:
        return f"({self.expression})"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_group(self)


class NodeExprVariable(NodeExpr):
    """
    Ember Node: Expression :: Group
    Represents an AST node of a variable location
    """

    # -Constructor
    def __init__(self, location: Location, _id: str) -> None:
        super().__init__(location)
        self.id: str = _id

    # -Dunder Methods
    def __str__(self) -> str:
        return f"Id({self.id})"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_variable(self)


class NodeExprLiteral(NodeExpr):
    """
    Ember Node: Expression :: Literal
    Represents an AST node of a constant literal with it's value
    """

    # -Constructor
    def __init__(
        self, location: Location, _type: NodeExprLiteral.Type, value: bool | int
    ) -> None:
        super().__init__(location)
        self.type: NodeExprLiteral.Type = _type
        self.value: bool | int = value

    # -Dunder Methods
    def __str__(self) -> str:
        match self.type:
            case NodeExprLiteral.Type.Boolean:
                return f"Bool({self.value})"
            case NodeExprLiteral.Type.Integer:
                return f"Integer({self.value})"
        assert False

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_literal(self)

    # -Sub-Classes
    class Type(IntEnum):
        '''Literal Type'''
        Boolean = auto()
        Integer = auto()
