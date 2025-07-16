##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: DeclFunction            ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Sequence
from typing import Any
from .core import Node, NodeContainer
from .visitor import NodeVisitor
from ..datatype import Datatype


## Classes
class NodeDeclFunction(NodeContainer):
    """
    Ember Node: Declaration :: Function
    Represents an AST node of a function declaration
    """

    # -Constructor
    def __init__(
        self, _id: str, parameters: Sequence[NodeDeclFunction.Parameter],
        _type: Datatype, body: Sequence[Node]
    ) -> None:
        super().__init__(body)
        self.id: str = _id
        self.type: Datatype = _type
        self.parameters: Sequence[NodeDeclFunction.Parameter] = parameters

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_declaration_function(self)

    # -Properties
    @property
    def parameter_count(self) -> int:
        return len(self.parameters)

    # -Sub-Classes
    class Parameter:

        # -Constructor
        def __init__(self, _id: str, _type: Datatype) -> None:
            self.id: str = _id
            self.type: Datatype = _type
