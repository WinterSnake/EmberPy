##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## AST: Printers                 ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING
from .unresolved import (
    AST_LITERAL_TYPES,
    UnresolvedNodeVisitor,
    UnresolvedTypeNode,
    UnresolvedModifierNode,
    UnresolvedFlowNode,
    UnresolvedAssignmentNode,
    UnresolvedBinaryNode,
    UnresolvedUnaryPrefixNode,
    UnresolvedUnaryPostfixNode,
    UnresolvedLiteralNode,
)

if TYPE_CHECKING:
    from .unresolved import (
        UnresolvedNode,
        UnresolvedUnitNode,
        UnresolvedFunctionNode,
        UnresolvedVariableNode,
        UnresolvedBlockNode,
        UnresolvedConditionalNode,
        UnresolvedWhileNode,
        UnresolvedDoNode,
        UnresolvedForNode,
        UnresolvedReturnNode,
        UnresolvedExprNode,
        UnresolvedGroupNode,
        UnresolvedIdentifierNode,
        UnresolvedEmptyNode,
    )


## Classes
class UnresolvedNodePrinter(UnresolvedNodeVisitor[str]):
    """
    A diagnostic visitor that transforms an Unresolved AST into a human-readable string.

    This printer is designed for the 'Unresolved' phase of the Ember compiler, where
    identifiers are not yet bound and C-style ambiguities (like type-casts vs. 
    multiplications) are still present in the tree.
    """

    # -Constructor
    def __init__(self) -> None:
        self.indent: int = 0

    # -Instance Methods: Visitor
    def visit_type(self, node: UnresolvedTypeNode) -> str:
        match node.kind:
            case UnresolvedTypeNode.Kind.Void:
                return "void"
            case UnresolvedTypeNode.Kind.Boolean:
                return "bool"
            case UnresolvedTypeNode.Kind.Int8:
                return "int8"
            case UnresolvedTypeNode.Kind.Int16:
                return "int16"
            case UnresolvedTypeNode.Kind.Int32:
                return "int32"
            case UnresolvedTypeNode.Kind.Int64:
                return "int64"
            case UnresolvedTypeNode.Kind.UInt8:
                return "uint8"
            case UnresolvedTypeNode.Kind.UInt16:
                return "uint16"
            case UnresolvedTypeNode.Kind.UInt32:
                return "uint32"
            case UnresolvedTypeNode.Kind.UInt64:
                return "uint64"

    def visit_modifier(self, node: UnresolvedModifierNode) -> str:
        match node.kind:
            case UnresolvedModifierNode.Kind.Const:
                return f"const"

    def visit_decl_unit(self, node: UnresolvedUnitNode) -> str:
        EMPTY = f"[Unit: {node.location.file} -- Empty]"
        if not node.nodes:
            return EMPTY
        nodes: list[str] = []
        for _node in node.nodes:
            if (_str := self.visit(_node)) != '':
                nodes.append(_str)
        if not nodes:
            return EMPTY
        return '\n'.join((f"[Unit: {node.location.file}]", *nodes))

    def visit_decl_function(self, node: UnresolvedFunctionNode) -> str:
        header = f"{self._get_indent()}Function Decl[Name={node.name} ; Return="
        ret_type, ret_modifiers = self._get_type_chain(node.return_type)
        ret_modifier_str = ','.join(ret_modifiers) if ret_modifiers else "None"
        header += f"{{Type={ret_type} ; Modifiers={ret_modifier_str}}}]"
        self.indent += 1
        # -Parameters
        parameters_str: str
        if node.arity == 0:
            parameters_str = f"{self._get_indent()}Parameters=None"
        else:
            parameters: list[str] = []
            for parameter in node.parameters:
                param_type, param_modifiers = self._get_type_chain(parameter.type)
                param_modifiers_str = ','.join(param_modifiers) if param_modifiers else "None"
                parameter_str = f"{self._get_indent()}Parameter={{Type={param_type} ; Modifier={param_modifiers_str}}} {parameter.name}"
                if parameter.has_initializer:
                    parameter_str += f" = {self.visit(parameter.initializer)}"
                parameters.append(parameter_str)
            parameters_str = '\n'.join(parameters)
        # -Body
        self.indent += 1
        body = self.visit(node.body)
        self.indent -= 2
        return '\n'.join((header, parameters_str, body))

    def visit_decl_variable(self, node: UnresolvedVariableNode) -> str:
        base_type, modifiers = self._get_type_chain(node.type)
        modifier_str = ','.join(modifiers) if modifiers else "None"
        header = f"{self._get_indent()}Variable Decl[Type={base_type} ; Modifiers={modifier_str}]"
        entries = []
        self.indent += 1
        for entry in node.entries:
            entry_str = f"{self._get_indent()}Entry: {entry.name}"
            if entry.has_initializer:
                entry_str += f" = {self.visit(entry.initializer)}"
            entries.append(entry_str)
        self.indent -= 1
        return '\n'.join((header, *entries))

    def visit_stmt_block(self, node: UnresolvedBlockNode) -> str:
        header = f"{self._get_indent()}{{"
        nodes: list[str] = []
        self.indent += 2
        for _node in node.nodes:
            if (_str := self.visit(_node)) != '':
                nodes.append(_str)
        self.indent -= 2
        footer = f"{self._get_indent()}}}"
        return '\n'.join((header, *nodes, footer))

    def visit_stmt_conditional(self, node: UnresolvedConditionalNode) -> str:
        header = f"{self._get_indent()}if ({self.visit(node.condition)})"
        self.indent += 1
        output = [header, self.visit(node.if_branch)]
        self.indent -= 1
        if node.has_else_branch:
            output.append(f"{self._get_indent()}else")
            self.indent += 1
            output.append(self.visit(node.else_branch))
            self.indent -= 1
        return '\n'.join(output)

    def visit_stmt_while(self, node: UnresolvedWhileNode) -> str:
        header = f"{self._get_indent()}while ({self.visit(node.condition)})"
        self.indent += 1
        body = self.visit(node.body)
        self.indent -= 1
        return '\n'.join((header, body))

    def visit_stmt_do(self, node: UnresolvedDoNode) -> str:
        header = f"{self._get_indent()}do"
        self.indent += 1
        body = self.visit(node.body)
        self.indent -= 1
        return '\n'.join((
            header, body,
            f"{self._get_indent()}while ({self.visit(node.condition)})"
        ))

    def visit_stmt_for(self, node: UnresolvedForNode) -> str:
        init = self.visit(node.initializer) if node.has_initializer else ""
        condition = self.visit(node.condition)
        inc = self.visit(node.increment) if node.has_increment else ""
        header = f"{self._get_indent()}for ({init};{condition};{inc})"
        self.indent += 1
        body = self.visit(node.body)
        self.indent -= 1
        return '\n'.join((header, body))

    def visit_stmt_flow(self, node: UnresolvedFlowNode) -> str:
        flow_str: str
        match node.kind:
            case UnresolvedFlowNode.Kind.Break:
                flow_str = "break"
            case UnresolvedFlowNode.Kind.Continue:
                flow_str = "continue"
        return f"{self._get_indent()}{flow_str}"

    def visit_stmt_return(self, node: UnresolvedReturnNode) -> str:
        output = f"{self._get_indent()}return"
        if not node.has_expression:
            return output
        return f"{output} {self.visit(node.expression)}"

    def visit_stmt_expression(self, node: UnresolvedExprNode) -> str:
        if not node.has_expression:
            return ''
        return f"{self._get_indent()}{self.visit(node.expression)}"

    def visit_expr_group(self, node: UnresolvedGroupNode) -> str:
        inner = self.visit(node.inner)
        if not node.has_target:
            return f"({inner})"
        return f"({inner} -> [{self.visit(node.target)}])"

    def visit_expr_assignment(self, node: UnresolvedAssignmentNode) -> str:
        l_value = self.visit(node.l_value)
        r_value = self.visit(node.r_value)
        match node.operator:
            case UnresolvedAssignmentNode.Operator.Eq:
                return f"({l_value} = {r_value})"
            case UnresolvedAssignmentNode.Operator.AddEq:
                return f"({l_value} += {r_value})"
            case UnresolvedAssignmentNode.Operator.SubEq:
                return f"({l_value} -= {r_value})"
            case UnresolvedAssignmentNode.Operator.MulEq:
                return f"({l_value} *= {r_value})"
            case UnresolvedAssignmentNode.Operator.DivEq:
                return f"({l_value} /= {r_value})"
            case UnresolvedAssignmentNode.Operator.ModEq:
                return f"({l_value} %= {r_value})"
            case UnresolvedAssignmentNode.Operator.BitXorEq:
                return f"({l_value} ^= {r_value})"
            case UnresolvedAssignmentNode.Operator.BitAndEq:
                return f"({l_value} &= {r_value})"
            case UnresolvedAssignmentNode.Operator.BitOrEq:
                return f"({l_value} |= {r_value})"
            case UnresolvedAssignmentNode.Operator.ShiftLEq:
                return f"({l_value} <<= {r_value})"
            case UnresolvedAssignmentNode.Operator.ShiftREq:
                return f"({l_value} >>= {r_value})"

    def visit_expr_binary(self, node: UnresolvedBinaryNode) -> str:
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        match node.operator:
            # -Math
            case UnresolvedBinaryNode.Operator.Add:
                return f"({lhs} + {rhs})"
            case UnresolvedBinaryNode.Operator.Sub:
                return f"({lhs} - {rhs})"
            case UnresolvedBinaryNode.Operator.Mul:
                return f"({lhs} * {rhs})"
            case UnresolvedBinaryNode.Operator.Div:
                return f"({lhs} / {rhs})"
            case UnresolvedBinaryNode.Operator.Mod:
                return f"({lhs} % {rhs})"
            # -Bitwise
            case UnresolvedBinaryNode.Operator.BitXor:
                return f"({lhs} ^ {rhs})"
            case UnresolvedBinaryNode.Operator.BitAnd:
                return f"({lhs} & {rhs})"
            case UnresolvedBinaryNode.Operator.BitOr:
                return f"({lhs} | {rhs})"
            case UnresolvedBinaryNode.Operator.ShiftL:
                return f"({lhs} << {rhs})"
            case UnresolvedBinaryNode.Operator.ShiftR:
                return f"({lhs} >> {rhs})"
            # -Comparisons
            case UnresolvedBinaryNode.Operator.LogOr:
                return f"({lhs} or {rhs})"
            case UnresolvedBinaryNode.Operator.LogAnd:
                return f"({lhs} and {rhs})"
            case UnresolvedBinaryNode.Operator.Eq:
                return f"({lhs} == {rhs})"
            case UnresolvedBinaryNode.Operator.NtEq:
                return f"({lhs} != {rhs})"
            case UnresolvedBinaryNode.Operator.Lt:
                return f"({lhs} < {rhs})"
            case UnresolvedBinaryNode.Operator.Gt:
                return f"({lhs} > {rhs})"
            case UnresolvedBinaryNode.Operator.LtEq:
                return f"({lhs} <= {rhs})"
            case UnresolvedBinaryNode.Operator.GtEq:
                return f"({lhs} >= {rhs})"

    def visit_expr_unary_prefix(self, node: UnresolvedUnaryPrefixNode) -> str:
        operand = self.visit(node.operand)
        match node.operator:
            # -Math
            case UnresolvedUnaryPrefixNode.Operator.NumericalNegate:
                return f"(-{operand})"
            case UnresolvedUnaryPrefixNode.Operator.LogicalNegate:
                return f"(!{operand})"
            case UnresolvedUnaryPrefixNode.Operator.BitwiseNegate:
                return f"(~{operand})"
            # -Typing
            case UnresolvedUnaryPrefixNode.Operator.Pointer:
                return f"*{operand}"
            case UnresolvedUnaryPrefixNode.Operator.AddressOf:
                return f"(@{operand})"
            case UnresolvedUnaryPrefixNode.Operator.Dereference:
                return f"({operand}.*)"

    def visit_expr_unary_postfix(self, node: UnresolvedUnaryPostfixNode) -> str:
        head = self.visit(node.head)
        arguments = ','.join(self.visit(argument) for argument in node.arguments)
        match node.kind:
            case UnresolvedUnaryPostfixNode.Kind.Call:
                return f"{head}({arguments})"

    def visit_expr_literal(self, node: UnresolvedLiteralNode) -> str:
        return str(node.value)

    def visit_expr_identifier(self, node: UnresolvedIdentifierNode) -> str:
        return node.name

    def visit_expr_empty(self, node: UnresolvedEmptyNode) -> str:
        return ''

    # -Instance Methods: Helpers
    def _get_indent(self) -> str:
        return ' ' * self.indent

    def _get_type_chain(self, node: UnresolvedNode) -> tuple[str, list[str]]:
        match node:
            case UnresolvedModifierNode():
                base_type, modifiers = self._get_type_chain(node.target)
                modifiers.append(self.visit(node))
                return (base_type, modifiers)
            case _:
                return (self.visit(node), [])

    # -Static Methods
    @staticmethod
    def run(ast: UnresolvedNode) -> None:
        printer = UnresolvedNodePrinter()
        print(printer.visit(ast))
