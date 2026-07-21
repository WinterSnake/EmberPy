##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Diagnostics: Engine           ##
##-------------------------------##

## Imports
import sys
from typing import (
    TYPE_CHECKING,
    Any, Self, TextIO,
    assert_never
)
from .diagnostic import Diagnostic
from .source_map import SourceMap

if TYPE_CHECKING:
    from collections.abc import MutableSequence
    from ..core import Span


## Classes
class DiagnosticEngine:
    """
    Ember Diagnostic Engine

    Driver for logging, storing, and displaying diagnostics through compiler pipeline.
    """
    # -Constructor
    def __init__(self, source_map: SourceMap) -> None:
        self.source_map: SourceMap = source_map
        self.has_error = False
        self.has_warning = False
        self._diagnostics: MutableSequence[Diagnostic] = []

    # -Instance Methods: Display
    def display(
        self, fd: TextIO = sys.stderr,
        level: Diagnostic.Level = Diagnostic.Level.Warn
    ) -> None:
        '''Display all diagnostics to io; filter by level.'''
        for diagnostic in self._diagnostics:
            if diagnostic.level > level:
                continue
            formatted = self._format_diagnostic(diagnostic)
            print(formatted, file=fd)

    def _format_diagnostic(self, diagnostic: Diagnostic) -> str:
        '''Return formatted string of diagnostic report.'''
        source = self.source_map[diagnostic.location.id]
        # -Location
        location = str(source.path) if source.is_path else "<raw source>"
        row, column = source.resolve_location(diagnostic.location.start)
        location = f"{location}:{row}:{column}"
        # -Level
        level: str
        match diagnostic.level:
            case Diagnostic.Level.Error:
                level = "Error"
            case Diagnostic.Level.Warn:
                level = "Warning"
            case _:
                assert_never(diagnostic.level)
        level = f"{level}[{diagnostic.name}]"
        # -Message
        message = diagnostic.message
        if diagnostic.is_formatted:
            message = message.format(*diagnostic.args)
        return f"{location} {level}: {message}"

    # -Instance Methods: Diagnostic
    def error(self, code: Diagnostic.Code, location: Span, *args: Any) -> None:
        '''Create and report an `Error` diagnostic.'''
        self.report(Diagnostic(Diagnostic.Level.Error, code, location, *args))

    def warn(self, code: Diagnostic.Code, location: Span, *args: Any) -> None:
        '''Create and report a `Warn` diagnostic.'''
        self.report(Diagnostic(Diagnostic.Level.Warn, code, location, *args))

    def report(self, diagnostic: Diagnostic) -> None:
        '''Store diagnostic and flag necessary state change.'''
        self._diagnostics.append(diagnostic)
        match diagnostic.level:
            case Diagnostic.Level.Error:
                self.has_error = True
            case Diagnostic.Level.Warn:
                self.has_warning = True

    # -Class Methods
    @classmethod
    def new(cls) -> Self:
        return cls(SourceMap())

    # -Class Properties
    __slots__ = (
        "source_map",
        "has_error",
        "has_warning",
        "_diagnostics",
    )
