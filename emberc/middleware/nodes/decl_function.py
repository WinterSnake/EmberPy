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
        self._parameters: Sequence[int] | None = parameters

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_declaration_function(self)

    # -Properties
    @property
    def has_parameters(self) -> bool:
        if self._parameters is None:
            return False
        return True

    @property
    def parameters(self) -> Sequence[int]:
        assert self._parameters is not None
        return self._parameters
