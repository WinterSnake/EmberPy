##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Middleware: 3AC               ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING
from .transformer import TACTreeTransformer
from ...ir import (
    TACUnit,
    TACDeclare,
)

if TYPE_CHECKING:
    from ...ir import (
        TACInstruction,
        TACInstructionBlock,
    )

## Constants
__all__ = (
    "TACTreeTransformer",
    "linearize_tac_tree",
)


## Functions
def linearize_tac_tree(tac: TACInstructionBlock) -> TACUnit:
    """[Group Pass]Runs a pipeline of lowering passes to flatten tree-structured TAC into linear TAC."""
    instructions: list[TACInstruction] = []
    for instruction in tac:
        match instruction:
            case TACDeclare():
                continue
            case _:
                instructions.append(instruction)
    return TACUnit(instructions)
