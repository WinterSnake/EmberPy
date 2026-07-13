##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Backend: Interpreter          ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING, assert_never
from .environment import Environment
from .lvalue import LValueResolver
from ...ast import (
    AssignOperator,
    BinaryOperator,
)

if TYPE_CHECKING:
    from collections.abc import Sequence
    from .environment import INTERPRETER_VALUE
    from ...ast import (
        ResolvedNode,
        TypePrimitive,
        DeclUnitNode,
        DeclVariableNode,
        StmtExpressionNode,
        ExprAssignNode,
        ExprBinaryNode,
        ExprIntegerNode,
        ExprVariableNode,
    )
    from ...middleware import Symbol

## Constants
__all__ = ("TreeWalkInterpreter",)


## Classes
class TreeWalkInterpreter:
    """
    An AST visitor that evaluates nodes to execute the program.
    
    Tracks variables via an execution environment and leverages an 
    LValueResolver to handle assignments to mutable storage locations.
    """

    # -Constructor
    def __init__(
        self, symbols: Sequence[Symbol], environment: Environment
    ) -> None:
        self.environment: Environment = environment
        self.symbols = symbols
        self.lvalue_resolver = LValueResolver(self)

    # -Instance Methods
    # --Types--
    def visit_type_primitive(self, node: TypePrimitive) -> None:
        assert False, "Tried calling interpreter with a primitive type node"

    # --Declarations--
    def visit_decl_unit(self, node: DeclUnitNode) -> None:
        for child in node:
            print(self.environment)
            child.accept(self)

    def visit_decl_variable(self, node: DeclVariableNode) -> None:
        value: INTERPRETER_VALUE | None = None
        if node.has_initializer:
            value = node.initializer.accept(self)
        self.environment.declare(node.id, value)

    # --Statements--
    def visit_stmt_expression(self, node: StmtExpressionNode) -> None:
        value = node.expression.accept(self)
        print(value)

    # --Expressions--
    def visit_expr_assignment(self, node: ExprAssignNode) -> INTERPRETER_VALUE:
        l_value = node.l_value.accept(self.lvalue_resolver)
        r_value = node.r_value.accept(self)
        match node.operator:
            case AssignOperator.Eq:
                l_value.set(self.environment, r_value)
            case _:
                assert_never(node.operator)
        return l_value.get(self.environment)

    def visit_expr_binary(self, node: ExprBinaryNode) -> INTERPRETER_VALUE:
        lhs = node.lhs.accept(self)
        rhs = node.rhs.accept(self)
        match node.operator:
            case BinaryOperator.Add:
                return lhs + rhs
            case BinaryOperator.Sub:
                return lhs - rhs
            case BinaryOperator.Mul:
                return lhs * rhs
            case BinaryOperator.Div:
                return lhs // rhs
            case BinaryOperator.Mod:
                return lhs % rhs
            case _:
                assert_never(node.operator)

    def visit_expr_integer(self, node: ExprIntegerNode) -> int:
        return node.value

    def visit_expr_variable(self, node: ExprVariableNode) -> INTERPRETER_VALUE:
        return self.environment[node.id]

    # -Static Methods
    @staticmethod
    def run(ast: ResolvedNode, symbols: Sequence[Symbol]) -> None:
        env = Environment.default
        ast.accept(Interpreter(symbols, env))

    # -Class Properties
    __slots__ = ("symbols", "environment", "lvalue_resolver")
