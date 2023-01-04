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
from typing import ClassVar, TextIO

from frontend import Node, ExpressionNode, ValueNode


## Functions
def graph_ast(
    nodes: list[Node], file: Path, dot_format: str = 'dot',
    generate_image: bool = True, image_format: str = 'png'
) -> Path:
    """Use Graphviz Visitor to output AST to a DOT file
    Will return the dot file if generate_image is false
    Will return the image file if generate_image is true"""
    file = file.with_suffix('.' + dot_format)
    graph_visitor: Node.Visitor = GraphvizVisitor()
    fp: TextIO = file.open('w')
    fp.write("digraph {\n")
    for node in nodes:
        _, text = node.visit(graph_visitor)
        fp.writelines(text)
    fp.write("}\n")
    fp.close()
    # -Generate output file/s
    if not generate_image:
        return file
    image_file: Path = file.with_suffix('.' + image_format)
    with image_file.open('w') as f:
        subprocess.run(["dot", str(file), f"-T{image_format}"], stdout=f)
    return image_file


## Classes
class GraphvizVisitor:
    """
    Graphviz AST Visitor
    Writes Graphviz DOT instructions based on node visited
    """

    # -Instance Methods
    def visit_expression_node(
        self, node: ExpressionNode
    ) -> tuple[int, tuple[str, ...]]:
        '''Creates node with binary expression as label
        and recursively descends down lhs and rhs nodes'''
        _id: int = self.id
        text: list[str] = []
        lhs: tuple[int, tuple[str]] = node.lhs.visit(self)
        rhs: tuple[int, tuple[str]] = node.rhs.visit(self)
        match node.operator:
            case ExpressionNode.Type.ADD:
                text.append(f"\tnode{_id}[label=\"+\"]\n")
            case ExpressionNode.Type.SUB:
                text.append(f"\tnode{_id}[label=\"-\"]\n")
            case ExpressionNode.Type.MUL:
                text.append(f"\tnode{_id}[label=\"*\"]\n")
            case ExpressionNode.Type.DIV:
                text.append(f"\tnode{_id}[label=\"/\"]\n")
            case ExpressionNode.Type.MOD:
                text.append(f"\tnode{_id}[label=\"%\"]\n")
            case _:
                # -TODO: Throw error
                pass
        text.extend([
            *lhs[1],
            *rhs[1],
            f"\tnode{_id} -> node{lhs[0]}\n"
            f"\tnode{_id} -> node{rhs[0]}\n"
        ])
        return (_id, tuple(text))

    def visit_value_node(self, node: ValueNode) -> tuple[int, tuple[str, ...]]:
        '''Creates basic node with numeric literal value as label'''
        _id: int = self.id
        text: str = f"\tnode{_id}[label=\"{node.value}\"]\n"
        return (_id, (text, ))
        

    # -Properties
    @property
    def id(self) -> int:
        _id: int = GraphvizVisitor.ID
        GraphvizVisitor.ID += 1
        return _id

    # -Class Properties
    ID: ClassVar[int] = 0
