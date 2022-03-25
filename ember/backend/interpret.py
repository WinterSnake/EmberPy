#!/usr/bin/python
##-------------------------------##
## Ember: Backend                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Interpret                     ##
##-------------------------------##

## Imports
from typing import Any

from frontend.node import NodeBase


## Functions
def interpret_ast(nodes: list[NodeBase]) -> int:
    """Interpret an ast"""
    for node in nodes:
        node.interpret()
    return 0
