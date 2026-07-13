##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Interpreter: LValueResolver   ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING, NoReturn, Protocol

if TYPE_CHECKING:
    from . import Interpreter
    from .environment import (
        INTERPRETER_VALUE,
        Environment
    )
    from ...ast import (
        ExprAssignNode,
        ExprBinaryNode,
        ExprIntegerNode,
        ExprVariableNode,
    )


## Classes
class Reference(Protocol):
    """LValue reference interface"""
    # -Instance Methods
    def get(self, environment: Environment) -> INTERPRETER_VALUE: ...
    def set(self, environment: Environment, value: INTERPRETER_VALUE) -> None: ...


@dataclass(frozen=True, slots=True)
class VariableReference:
    """LValue variable reference"""
    # -Instance Methods
    def get(self, environment: Environment) -> INTERPRETER_VALUE:
        return environment[self.id]

    def set(self, environment: Environment, value: INTERPRETER_VALUE) -> None:
        environment.assign(self.id, value)

    # -Properties
    id: int


class LValueResolver:
    """
    An AST visitor that resolves expressions to memory references (l-values).
    
    Ensures that expressions on the left-hand side of an assignment are valid 
    assignable targets (like variables) rather than evaluation values (like literals).
    """
    
    # -Constructor
    def __init__(self, host: Interpreter) -> None:
        self._host: Interpreter = host

    # -Instance Methods
    def visit_expr_assignment(self, node: ExprAssignNode) -> NoReturn:
        assert False, "Tried calling lvalue resolver with an assignment expr node"

    def visit_expr_binary(self, node: ExprBinaryNode) -> NoReturn:
        assert False, "Tried calling lvalue resolver with a binary expr node"

    def visit_expr_integer(self, node: ExprIntegerNode) -> NoReturn:
        assert False, "Tried calling lvalue resolver with an integer expr node"

    def visit_expr_variable(self, node: ExprVariableNode) -> Reference:
        return VariableReference(node.id)

    # -Class Properties
    __slots__ = ("_host",)
