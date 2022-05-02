#!/usr/bin/python
##-------------------------------##
## Ember: Plugins                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Graphviz                      ##
##-------------------------------##

## Imports
from typing import Any

import graphviz  #type: ignore


## Functions
def graph_ast(nodes: list[Any], *args: Any, **kwargs: Any) -> graphviz.Digraph:
    """Dump an ast for graphviz"""
    # -Internal Variables
    graph: graphviz.Diagraph = graphviz.Digraph(*args, **kwargs)
    id_: int = 0
    # -Internal Functions
    def dump_node(node: Any) -> int:
        '''Dump single node for graphviz'''
        # -ID
        nonlocal id_
        id__: int = id_
        id_ += 1
        # -Output
        if isinstance(node, int):
            graph.node(f"id{id__}", label=str(node))
        elif isinstance(node, dict):
            op: str = list(node.keys())[0]
            lhs: int = dump_node(node[op]['lhs'])
            rhs: int = dump_node(node[op]['rhs'])
            graph.node(f"id{id__}", label=op)
            graph.edge(f"id{id__}", f"id{lhs}")
            graph.edge(f"id{id__}", f"id{rhs}")
        return id__
    # -Body
    for node in nodes:
        dump_node(node)
    return graph
