##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node::Statement - Expression  ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import Any
from .core import Node
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeStmtBlock(Node):
    """
    Ember Statement Node: Block
    Represents a statement block node
    """

    # -Constructor
    def __init__(self, statements: Sequence[Node]) -> None:
        self.statements: Sequence[Node] = statements

    # -Dunder Methods
    def __str__(self) -> str:
        _str = ','.join(str(node) for node in statements)
        return f"{{ {_str} }}"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_block(self)
