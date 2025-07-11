##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Declaration             ##
##-------------------------------##

## Imports
from typing import Any
from .core import Node, NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeDeclVariable(Node):
    """
    Ember Node: Declaration :: Variable
    Represents an AST node of a variable declaration
    """

    # -Constructor
    def __init__(self, _id: str, initializer: NodeExpr | None) -> None:
        self.id: str = _id
        self.initializer: NodeExpr | None = initializer

    # -Dunder Methods
    def __str__(self) -> str:
        _str = f"{{Id({self.id})"
        if self.initializer:
            _str += f" = {self.initializer}"
        return _str + "}}"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_declaration_variable(self)


class NodeStmtExpression(Node):
    """
    Ember Node: Statement :: Expression
    Represents an AST node of a statement with an expression
    """

    # -Constructor
    def __init__(self, expression: NodeExpr) -> None:
        self.expression: NodeExpr = expression

    # -Dunder Methods
    def __str__(self) -> str:
        return str(self.expression)

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_expression(self)
