##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## 3AC: Transformer              ##
##-------------------------------##

## Imports
from collections.abc import Iterable
from typing import TYPE_CHECKING, NoReturn, get_args
from ...ir import (
    TACAddress,
    TACInstructionBlock,
    TACLiteral,
    TACTemporary,
    TACVariable,
    TACAssign,
    TACBinary,
    TACDeclare,
)

if TYPE_CHECKING:
    from ...ast import (
        TypePrimitive,
        DeclUnitNode,
        DeclVariableNode,
        StmtExpressionNode,
        ExprAssignNode,
        ExprBinaryNode,
        ExprIntegerNode,
        ExprVariableNode,
    )
    from ...ir import (
        TACInstruction,
        TACOperand,
    )

## Constants
type TACExprNode = tuple[TACOperand, TACInstructionBlock | None]


## Functions
def _operand_as_address(operand: TACOperand) -> TACAddress:
    assert isinstance(operand, get_args(TACAddress.__value__)), f"Expected TACAddress, got: {type(operand).__name__}"
    return operand  # type: ignore[no-any-return]


## Classes
class TACTreeTransformer:
    """
    TAC Lowering Pass [0]

    Traverses the AST and yields nested instructions/blocks that preserve local expressions,
    producing an intermediate tree structure ready for linearization.
    """

    # -Constructor
    def __init__(self) -> None:
        self._temporary: int = 0

    # -Instance Methods
    # --Types--
    def visit_type_primitive(self, node: TypePrimitive) -> NoReturn:
        assert False, "Tried calling 3AC tree transformer with a type node"

    # --Declarations--
    def visit_decl_unit(self, node: DeclUnitNode) -> TACInstructionBlock:
        instructions: list[TACInstruction] = []
        for child in node:
            c_inst = child.accept(self)
            if not c_inst:
                continue
            instructions.extend(c_inst)
        return TACInstructionBlock(instructions)

    def visit_decl_variable(self, node: DeclVariableNode) -> TACInstructionBlock:
        block: Iterable[TACInstruction] = []
        if node.has_initializer:
            i_tac, i_inst = node.initializer.accept(self)
            i_assign = TACAssign(TACVariable(node.id), i_tac)
            block = TACInstructionBlock.filter(i_inst, i_assign)
        return TACInstructionBlock([
            TACDeclare(node.id),
            *block,
        ])

    # --Statements--
    def visit_stmt_expression(self, node: StmtExpressionNode) -> TACInstructionBlock | None:
        _, e_block = node.expression.accept(self)
        return e_block

    # --Expressions--
    def visit_expr_assignment(self, node: ExprAssignNode) -> TACExprNode:
        l_tac, l_inst = node.l_value.accept(self)
        r_tac, r_inst = node.r_value.accept(self)
        l_tac = _operand_as_address(l_tac)
        return (
            r_tac,
            TACInstructionBlock([
                *TACInstructionBlock.filter(l_inst, r_inst),
                TACAssign(l_tac, r_tac),
            ])
        )

    def visit_expr_binary(self, node: ExprBinaryNode) -> TACExprNode:
        l_tac, l_inst = node.lhs.accept(self)
        r_tac, r_inst = node.rhs.accept(self)
        dest = TACTemporary(self.next_temporary)
        return (
            dest,
            TACInstructionBlock([
                *TACInstructionBlock.filter(l_inst, r_inst),
                TACBinary(dest, node.operator, l_tac, r_tac),
            ])
        )

    def visit_expr_integer(self, node: ExprIntegerNode) -> TACExprNode:
        return (TACLiteral(node.value), None)

    def visit_expr_variable(self, node: ExprVariableNode) -> TACExprNode:
        return (TACVariable(node.id), None)

    # -Static Methods
    @staticmethod
    def run(ast: DeclUnitNode) -> TACInstructionBlock:
        transformer = TACTreeTransformer()
        return ast.accept(transformer)

    # -Properties
    @property
    def next_temporary(self) -> int:
        _temporary = self._temporary
        self._temporary += 1
        return _temporary

    # -Class Properties
    __slots__ = ("_temporary",)
