##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Statement    ##
##-------------------------------##

## Imports
from collections.abc import Collection
from dataclasses import dataclass
from .node import UnresolvedNode
from .declaration import UnresolvedDeclNode, UnresolvedDeclVariableNode

## Constants
type BLOCK_TYPES = UnresolvedDeclNode | UnresolvedStmtNode


## Classes
class UnresolvedStmtNode(UnresolvedNode):
    """
    Ember Unresolved Node: Statement

    A base node for storing statement context
    """
    pass


@dataclass
class UnresolvedStmtEmptyNode(UnresolvedStmtNode):
    """
    Ember Unresolved Statement: Empty

    A no-op statement
    """
    pass


@dataclass
class UnresolvedStmtBlockNode(UnresolvedStmtNode):
    """
    Ember Unresolved Statement: Block

    A statement containing a list of inner declarations or statements
    """
    # -Properties
    body: Collection[BLOCK_TYPES]


@dataclass
class UnresolvedStmtExpressionNode(UnresolvedStmtNode):
    """
    Ember Unresolved Statement: Expression

    A statement containing a single expression
    """
    # -Properties
    expression: UnresolvedNode


@dataclass
class UnresolvedStmtConditionalNode(UnresolvedStmtNode):
    """
    Ember Unresolved Statement: Conditional

    A statement containing conditional if_branch and (optional)else_branch
    """
    # -Properties
    condition: UnresolvedNode
    if_branch: UnresolvedStmtNode
    _else_branch: UnresolvedStmtNode | None

    @property
    def has_else_branch(self) -> bool:
        return self._else_branch is not None

    @property
    def else_branch(self) -> UnresolvedStmtNode:
        assert self._else_branch is not None
        return self._else_branch


@dataclass
class UnresolvedStmtLoopWhileNode(UnresolvedStmtNode):
    """
    Ember Unresolved Statement: While

    A statement containing a while condition loop with body
    """
    # -Properties
    condition: UnresolvedNode
    body: UnresolvedStmtNode


@dataclass
class UnresolvedStmtLoopDoNode(UnresolvedStmtNode):
    """
    Ember Unresolved Statement: Do/While

    A statement containing a do/while condition loop with body
    """
    # -Properties
    condition: UnresolvedNode
    body: UnresolvedStmtNode


@dataclass
class UnresolvedStmtLoopForNode(UnresolvedStmtNode):
    """
    Ember Unresolved Statement: For

    A statement containing a for loop with (optional)initializer,
    conditions, (optional)increment, and body
    """
    # -Properties
    _initializer: UnresolvedNode | UnresolvedDeclVariableNode | None
    condition: UnresolvedNode
    _increment: UnresolvedNode | None
    body: UnresolvedStmtNode

    @property
    def has_initializer(self) -> bool:
        return self._initializer is not None

    @property
    def initializer(self) -> UnresolvedNode | UnresolvedDeclVariableNode:
        assert self._initializer is not None
        return self._initializer

    @property
    def has_increment(self) -> bool:
        return self._increment is not None

    @property
    def increment(self) -> UnresolvedNode:
        assert self._increment is not None
        return self._increment


@dataclass
class UnresolvedStmtReturnNode(UnresolvedStmtNode):
    """
    Ember Unresolved Statement: Return

    A statement containing a return with (optional)value
    """
    # -Properties
    _value: UnresolvedNode | None

    @property
    def has_value(self) -> bool:
        return self._value is not None

    @property
    def value(self) -> UnresolvedNode:
        assert self._value is not None
        return self._value
