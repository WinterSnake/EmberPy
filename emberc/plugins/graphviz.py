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
from typing import Any


## Functions
def graph_ast(ast: list[dict[str, Any]], file: Path) -> None:
    """"""
    # -Internal Variables
    fp: TextIO = file.open('w')
    node_counter: int = 0
    # -Internal Functions
    def dump_node(node: dict[str, Any]) -> int:
        ''''''
        nonlocal node_counter
        id_: int = node_counter
        node_counter += 1
        if 'value' in node:
            fp.write(f"\t\tnode{id_}[label=\"{node['value']}\"]\n")
        elif 'add' in node:
            lhs: int = dump_node(node['add']['lhs'])
            rhs: int = dump_node(node['add']['rhs'])
            fp.writelines((
                f"\t\tnode{id_}[label=\"+\"]\n",
                f"\t\tnode{id_} -> node{lhs}\n"
                f"\t\tnode{id_} -> node{rhs}\n"
            ))
        elif 'sub' in node:
            lhs: int = dump_node(node['sub']['lhs'])
            rhs: int = dump_node(node['sub']['rhs'])
            fp.writelines((
                f"\t\tnode{id_}[label=\"-\"]\n",
                f"\t\tnode{id_} -> node{lhs}\n"
                f"\t\tnode{id_} -> node{rhs}\n"
            ))
        elif 'mul' in node:
            lhs: int = dump_node(node['mul']['lhs'])
            rhs: int = dump_node(node['mul']['rhs'])
            fp.writelines((
                f"\t\tnode{id_}[label=\"*\"]\n",
                f"\t\tnode{id_} -> node{lhs}\n"
                f"\t\tnode{id_} -> node{rhs}\n"
            ))
        elif 'div' in node:
            lhs: int = dump_node(node['div']['lhs'])
            rhs: int = dump_node(node['div']['rhs'])
            fp.writelines((
                f"\t\tnode{id_}[label=\"/\"]\n",
                f"\t\tnode{id_} -> node{lhs}\n"
                f"\t\tnode{id_} -> node{rhs}\n"
            ))
        elif 'mod' in node:
            lhs: int = dump_node(node['mod']['lhs'])
            rhs: int = dump_node(node['mod']['rhs'])
            fp.writelines((
                f"\t\tnode{id_}[label=\"%\"]\n",
                f"\t\tnode{id_} -> node{lhs}\n"
                f"\t\tnode{id_} -> node{rhs}\n"
            ))
        else:
            # -TODO: Handle Error
            print(f"Unhandled node: {node}")
            return None  # type: ignore
        return id_

    # -Body
    fp.write("digraph {\n")
    for node in ast:
        dump_node(node)
    fp.write("}\n")
    fp.close()
    with file.with_suffix(".png").open('w') as f:
        subprocess.run(["dot", str(file), "-Tpng"], stdout=f)
