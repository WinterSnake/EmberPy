##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: StmtBlock               ##
##-------------------------------##

## Imports
from collections.abc import Sequence
from typing import Any
from .core import Node, NodeContainer
from .visitor import NodeVisitor


## Classes
class NodeStmtBlock(NodeContainer):
    """
    Ember Node: Statement :: Block
    Represents an AST node of a iterable collection of nodes
    """

    # -Constructor
    def __init__(self, body: Sequence[Node]) -> None:
        super().__init__(body)

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_block(self)
