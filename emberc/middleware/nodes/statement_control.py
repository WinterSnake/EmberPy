##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Control                 ##
##-------------------------------##

## Imports
from typing import Any, Sequence
from .core import Node, NodeContainer, NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeStmtBlock(NodeContainer):
    """
    Ember Node: Statement :: Block
    Represents an AST node of a block statement
    """

    # -Constructor
    def __init__(self, body: Sequence[Node]) -> None:
        super().__init__(body)

    # -Dunder Methods
    def __str__(self) -> str:
        return super().__str__()

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_block(self)

class NodeStmtConditional(Node):
    """
    Ember Node: Statement :: Block
    Represents an AST node of an if conditional statement
    """

    # -Constructor
    def __init__(
        self, condition: NodeExpr, body: Node, branch: Node | None
    ) -> None:
        self.condition: NodeExpr = condition
        self.body: Node = body
        self.branch: Node | None = branch

    # -Dunder Methods
    def __str__(self) -> str:
        return f"{{{self.body} if ({self.condition})}}"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_conditional(self)


class NodeStmtLoop(Node):
    """
    Ember Node: Statement :: Loop
    Represents an AST node of an while loop statement
    """

    # -Constructor
    def __init__(self, condition: NodeExpr, body: Node) -> None:
        self.condition: NodeExpr = condition
        self.body: Node = body

    # -Dunder Methods
    def __str__(self) -> str:
        return f"{{{self.body} until ({self.condition})}}"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_loop(self)
