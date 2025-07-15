##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: DeclVariable            ##
##-------------------------------##

## Imports
from typing import Any
from .core import Node, NodeExpr
from .visitor import NodeVisitor


## Classes
class NodeDeclVariable(Node):
    """
    Ember Node: Declaration :: Variable
    Represents an AST node of a variable declaration
    """

    # -Constructor
    def __init__(self, _id: int, initializer: NodeExpr | None) -> None:
        self.id: int = _id
        self._initializer: NodeExpr | None = initializer

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_declaration_variable(self)

    # -Properties
    @property
    def has_initializer(self) -> bool:
        return self._initializer is not None

    @property
    def initializer(self) -> NodeExpr:
        assert self._initializer is not None
        return self._initializer
