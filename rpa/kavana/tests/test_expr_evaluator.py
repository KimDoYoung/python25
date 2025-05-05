import pytest
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.variable_manager import VariableManager
from tests.helper_func import get_tokens
from lib.core.token_type import TokenType
from lib.core.datatypes.kavana_datatype import Integer, Boolean, String


@pytest.fixture
def evaluator():
    return ExprEvaluator(variable_manager=VariableManager())


def eval_expr(expr: str, evaluator: ExprEvaluator):
    tokens, start_idx = get_tokens(expr)
    return evaluator.evaluate(tokens[start_idx:])


def test_simple_addition(evaluator):
    result = eval_expr("1 + 2", evaluator)
    assert result.data.value == 3
    assert result.type == TokenType.INTEGER


def test_string_concatenation(evaluator):
    result = eval_expr('"hello" + " world"', evaluator)
    assert result.data.value == "hello world"
    assert result.type == TokenType.STRING


def test_boolean_logic(evaluator):
    result = eval_expr("True AND False", evaluator)
    assert result.data.value is False
    assert result.type == TokenType.BOOLEAN


def test_unary_minus(evaluator):
    result = eval_expr("-5", evaluator)
    assert result.data.value == -5
    assert result.type == TokenType.INTEGER


def test_comparison_equal(evaluator):
    result = eval_expr("10 == 10", evaluator)
    assert result.data.value is True
    assert result.type == TokenType.BOOLEAN


def test_arithmetic_precedence(evaluator):
    result = eval_expr("2 + 3 * 4", evaluator)  # 2 + (3 * 4) = 14
    assert result.data.value == 14


def test_parentheses(evaluator):
    result = eval_expr("(2 + 3) * 4", evaluator)  # (2 + 3) * 4 = 20
    assert result.data.value == 20
