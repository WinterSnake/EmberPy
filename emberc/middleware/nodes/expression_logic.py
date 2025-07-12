##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression - Logic      ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any, Sequence
from .core import NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Functions
def _get_operator_str(_type: NodeExprLogical.Type) -> str:
    """Returns the char/string of a given binary operator"""
    match _type:
        case NodeExprLogical.Type.Or:
            return 'and'
        case NodeExprLogical.Type.And:
            return 'or'


## Classes
class NodeExprAssignment(NodeExpr):
    """
    Ember Node: Expression :: Assignment
    Represents an AST node of an assignment expression
    """

    # -Constructor
    def __init__(self, location: Location, _id: str, expression: NodeExpr) -> None:
        super().__init__(location)
        self.id: str = _id
        self.expression: NodeExpr = expression

    # -Dunder Methods
    def __str__(self) -> str:
        return f"(Id({self.id}) = {self.expression})"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_assignment(self)


class NodeExprCall(NodeExpr):
    """
    Ember Node: Expression :: Call
    Represents an AST node of a call expression with arguments
    """

    # -Constructor
    def __init__(
        self, location: Location, callee: NodeExpr,
        arguments: Sequence[NodeExpr] | None
    ) -> None:
        super().__init__(location)
        self.callee: NodeExpr = callee
        self.arguments: Sequence[NodeExpr] | None = arguments

    # -Dunder Methods
    def __str__(self) -> str:
        if self.has_arguments:
            assert self.arguments is not None
            args = ','.join(str(node) for node in self.arguments)
        else:
            args = ''
        return f"{{{self.callee}({args})}}"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_call(self)

    # -Properties
    @property
    def has_arguments(self) -> bool:
        return self.arguments is not None

    @property
    def argument_count(self) -> int:
        if self.arguments is None:
            return 0
        return len(self.arguments)


class NodeExprLogical(NodeExpr):
    """
    Ember Node: Expression :: Logical
    Represents an AST node of a logical operator
    """

    # -Constructor
    def __init__(
        self, location: Location, operator: NodeExprLogical.Type,
        lhs: NodeExpr, rhs: NodeExpr
    ) -> None:
        super().__init__(location)
        self.operator: NodeExprLogical.Type = operator
        self.lhs: NodeExpr = lhs
        self.rhs: NodeExpr = rhs

    # -Dunder Methods
    def __str__(self) -> str:
        return f"(({self.lhs}) {self.operator.name} ({self.rhs}))"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_logical(self)

    # -Sub-Classes
    class Type(IntEnum):
        '''Logical Operator Type'''
        And = auto()
        Or = auto()
