##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Middleware                    ##
##-------------------------------##

## Imports
from .datatype import Datatype, get_datatype_from_token

## Constants
__all__: tuple[str, ...] = (
    "Datatype",
    "get_datatype_from_token",
)
