#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Plugins: Graphviz             ##
##-------------------------------##

## Imports
import subprocess
from pathlib import Path
from typing import Any, TextIO

from frontend import Node, ExpressionNode, ValueNode


## Functions
def graph_ast(nodes: list[Node], file: Path) -> None:
    """"""
    graph = GraphvizVisitor()
    fp: TextIO = file.open('w')
    fp.write("digraph {\n")
    for node in nodes:
        node.visit(graph, fp)
    fp.write("}\n")
    fp.close()
    with file.with_suffix('.png').open('w') as f:
        subprocess.run(["dot", str(file), "-Tpng"], stdout=f)


## Classes
class GraphvizVisitor(Node.Visitor):
    """"""

    # -Constructor
    def __init__(self, _current_id: int = 0) -> None:
        self._current_id: int = _current_id

    # -Instance Methods
    def visit_expression_node(self, node: ExpressionNode, fp: TextIO) -> int:
        ''''''
        _id: int = self.id
        lhs: int = node.lhs.visit(self, fp)
        rhs: int = node.rhs.visit(self, fp)
        match node.operator:
            case ExpressionNode.Type.ADD:
                fp.write(f"\tnode{_id}[label=\"+\"]\n")
            case ExpressionNode.Type.SUB:
                fp.write(f"\tnode{_id}[label=\"-\"]\n")
            case ExpressionNode.Type.MUL:
                fp.write(f"\tnode{_id}[label=\"*\"]\n")
            case ExpressionNode.Type.DIV:
                fp.write(f"\tnode{_id}[label=\"/\"]\n")
            case ExpressionNode.Type.MOD:
                fp.write(f"\tnode{_id}[label=\"%\"]\n")
            case _:
                # -TODO: Throw error
                pass
        fp.writelines((
            f"\tnode{_id} -> node{lhs}\n"
            f"\tnode{_id} -> node{rhs}\n"
        ))
        return _id


    def visit_value_node(self, node: ValueNode, fp: TextIO) -> int:
        ''''''
        _id: int = self.id
        fp.write(f"\tnode{_id}[label=\"{node.value}\"]\n")
        return _id
        

    # -Properties
    @property
    def id(self) -> int:
        _id: int = self._current_id
        self._current_id += 1
        return _id
