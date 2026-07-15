##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Middleware: 3AC               ##
##-------------------------------##

## Imports
from collections.abc import Iterator
from typing import TYPE_CHECKING
from .transformer import TACTreeTransformer
from ...ir import (
    TACUnit,
    TACVisitor,
    TACInstruction,
)

if TYPE_CHECKING:
    from ...ir import (
        TACInstructionBlock,
        TACAssign,
        TACBinary,
        TACDeclare,
    )

## Constants
__all__ = (
    "TACTreeTransformer",
    "linearize_tac_tree",
)


## Functions
def linearize_tac_tree(tac: TACInstructionBlock) -> TACUnit:
    """[Group Pass]Runs a pipeline of lowering passes to flatten tree-structured TAC into linear TAC."""
    return TACLinearTransformer.run(tac)


## Classes
class TACLinearTransformer(TACVisitor[TACInstruction | None]):
    """
    TAC Lowering Pass [1]

    Traverses the intermediate tree structure and flattens nested instructions.
    """

    # -Instance Methods: Visitor
    def visit_assignment(self, tac: TACAssign) -> TACInstruction:
        return tac

    def visit_binary(self, tac: TACBinary) -> TACInstruction:
        return tac

    def visit_declare(self, tac: TACDeclare) -> TACInstruction:
        return tac

    # -Instance Methods: Helpers
    def visit_block(self, tac: TACInstructionBlock) -> Iterator[TACInstruction]:
        for instruction in tac:
            result = self.visit(instruction)
            if result:
                yield result

    # -Static Methods
    @staticmethod
    def run(tac: TACInstructionBlock) -> TACUnit:
        instructions: list[TACInstruction] = []
        transformer = TACLinearTransformer()
        for instruction in transformer.visit_block(tac):
            instructions.append(instruction)
        return TACUnit(instructions)
