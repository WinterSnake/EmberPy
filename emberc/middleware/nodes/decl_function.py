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
    def __init__(
        self, _id: int, parameters: Sequence[int] | None, body: Sequence[Node]
    ) -> None:
        super().__init__(body)
        self.id: int = _id
        self.parameters: Sequence[int] | None = parameters

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_declaration_function(self)

    # -Properties
    @property
    def parameter_count(self) -> int:
        if self.parameters is None:
            return 0
        return len(self.parameters)
