##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Diagnostic: Engine            ##
##-------------------------------##

## Imports
from typing import Self
from .source_map import SourceMap


## Classes
class DiagnosticEngine:
    """
    Central hub for managing compiler diagnostics, error reporting, and pipeline tracing.
    
    Utilizes a `SourceMap` to link errors and warnings back to their original 
    source locations, and provides hooks for debugging individual compiler passes.
    """

    # -Constructor
    def __init__(self, source_map: SourceMap) -> None:
        self.source_map: SourceMap = source_map
        self.has_error: bool = False

    # -Instance Methods
    def error(self, msg: str) -> None:
        print(f"Error: {msg}")
        self.has_error = True

    # -Class Methods
    @classmethod
    def new(cls) -> Self:
        return cls(SourceMap())
