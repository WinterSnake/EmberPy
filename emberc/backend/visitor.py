#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Backend: Node Visitor         ##
##-------------------------------##

## Imports
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..frontend.node import Node, NodeDefinition, NodeAssignment, NodeBinExpr, NodeLiteral

## Constants
__all__: tuple[str, ...] = ("NodeVisitor",)


## Classes
class NodeVisitor(ABC):
    """"""

    # -Instance Methods
    @abstractmethod
    def visit_definition(self, node: NodeDefinition) -> Node: ...
    @abstractmethod
    def visit_assignment(self, node: NodeAssignment) -> Node: ...
    @abstractmethod
    def visit_binexpr(self, node: NodeBinExpr) -> Node: ...
    @abstractmethod
    def visit_literal(self, node: NodeLiteral) -> Node: ...
