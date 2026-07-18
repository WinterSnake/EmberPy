##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## IR                            ##
##-------------------------------##

## Imports
from .tac import (
    TACUnit,
    TACVisitor,
    TACAddress,
    TACOperand,
    TACLiteral,
    TACTemporary,
    TACVariable,
    TACInstruction,
    TACAssign,
    TACBinary,
    TACDeclare,
)


## Constants
__all__ = (
    # -3AC
    "TACUnit",
    "TACVisitor",
    # -3AC: Operand
    "TACAddress",
    "TACOperand",
    "TACLiteral",
    "TACTemporary",
    "TACVariable",
    # -3AC: Instruction
    "TACInstruction",
    "TACAssign",
    "TACBinary",
    "TACDeclare",
)
