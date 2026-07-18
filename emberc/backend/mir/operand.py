##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## MIR: Operand                  ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .register import MIRRegister

## Constants
type MIROperand = MIRRegister | int
