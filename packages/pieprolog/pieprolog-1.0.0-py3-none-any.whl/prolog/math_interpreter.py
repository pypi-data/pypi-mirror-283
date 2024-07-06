from .expression import Visitor
from .errors import InterpreterError


class MathInterpreter(Visitor):
    """Arithmetic Interpreter

    This class walks the expression tree and evaluates returning
    the computed value.
    """

    def _evaluate_expr(self, expr):
        return expr.accept(self)

    def _compute_binary_operand(self, left, operand, right):
        if type(left) != type(right):
            raise InterpreterError(
                f'left {left} and right {right} operand must have the same type'
            )  # noqa
        if operand == '*':
            return left.multiply(right)
        elif operand == '/':
            return left.divide(right)
        elif operand == '+':
            return left.add(right)
        elif operand == '-':
            return left.substract(right)
        else:
            raise InterpreterError(f'Invalid binary operand {operand}')

    def visit_binary(self, expr):
        left = self._evaluate_expr(expr.left)
        right = self._evaluate_expr(expr.right)

        return self._compute_binary_operand(left, expr.operand, right)

    def visit_primary(self, expr):
        return expr.exp
