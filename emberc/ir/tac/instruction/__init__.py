##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## IR 3AC: Instruction           ##
##-------------------------------##

## Imports
from .assign import TACAssign
from .binary import TACBinary
from .declare import TACDeclare


## Constants
__all__ = (
    "TACInstruction",
    "TACAssign",
    "TACBinary",
    "TACDeclare",
)
type TACInstruction = TACAssign | TACBinary | TACDeclare
