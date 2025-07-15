##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: DeclFunction            ##
##-------------------------------##

## Imports
from collections.abc import Sequence
from typing import Any
from .core import Node, NodeContainer
from .visitor import NodeVisitor


## Classes
class NodeDeclFunction(NodeContainer):
    """
    Ember Node: Declaration :: Function
    Represents an AST node of a function declaration
    """

    # -Constructor
    def __init__(self, _id: int, body: Sequence[Node]) -> None:
        super().__init__(body)
        self.id: int = _id

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_declaration_function(self)
