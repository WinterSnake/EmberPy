##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## IR                            ##
##-------------------------------##

## Imports
from .tac import (
    TACUnit,
    TACAddress,
    TACOperand,
    TACLiteral,
    TACTemporary,
    TACVariable,
    TACInstruction,
    TACInstructionBlock,
    TACAssign,
    TACBinary,
    TACDeclare,
)


## Constants
__all__ = (
    "TACUnit",
    # -3AC: Operand
    "TACAddress",
    "TACOperand",
    "TACLiteral",
    "TACTemporary",
    "TACVariable",
    # -3AC: Instruction
    "TACInstruction",
    "TACInstructionBlock",
    "TACAssign",
    "TACBinary",
    "TACDeclare",
)
