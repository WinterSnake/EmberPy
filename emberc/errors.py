##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Errors                        ##
##-------------------------------##

## Imports
from .location import Location


## Classes
class EmberError(Exception):
    """A general error report for Ember"""
    
    # -Constructor
    def __init__(self, location: Location, message: str) -> None:
        super().__init__(f"[{location}]{message}")
        self.location = location


class EmberLexerError(EmberError):
    """An error report for Ember lexing"""


class EmberParserError(EmberError):
    """An error report for Ember parsing"""
