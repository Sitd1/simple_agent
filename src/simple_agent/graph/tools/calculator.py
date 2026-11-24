import ast
import operator
from collections.abc import Callable

from langchain_core.tools import tool

from simple_agent.graph.schemas import CalculateInput

_BINARY_OPS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}
_MAX_EXPONENT = 1000


def _evaluate(node: ast.AST) -> float:
    """Безопасно вычисляет AST: только числа и арифметика, никакого eval."""
    if (
        isinstance(node, ast.Constant)
        and isinstance(node.value, int | float)
        and not isinstance(node.value, bool)
    ):
        return node.value
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_evaluate(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPS:
        left, right = _evaluate(node.left), _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > _MAX_EXPONENT:
            raise ValueError(f"слишком большая степень (максимум {_MAX_EXPONENT})")
        return _BINARY_OPS[type(node.op)](left, right)
    raise ValueError("допустимы только числа, скобки и операторы + - * / // % **")


@tool(args_schema=CalculateInput)
def calculate(expression: str) -> str:
    """Вычисляет арифметическое выражение и возвращает результат."""
    try:
        result = _evaluate(ast.parse(expression, mode="eval").body)
    except ZeroDivisionError:
        return "Ошибка: деление на ноль"
    except (ValueError, SyntaxError) as error:
        return f"Ошибка: {error}"
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    return str(result)
