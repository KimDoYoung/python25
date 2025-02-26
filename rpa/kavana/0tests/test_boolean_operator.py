import pytest
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.variable_manager import VariableManager

def eval_expr(expression: str):
    var_manager = VariableManager()
    evaluator = ExprEvaluator(expression, var_manager)
    return evaluator.evaluate()

def test_boolean_and():
    # True and False → False, True and True → True
    assert eval_expr("True and False") is False
    assert eval_expr("True and True") is True

def test_boolean_or():
    # False or True → True, False or False → False
    assert eval_expr("False or True") is True
    assert eval_expr("False or False") is False

def test_boolean_not():
    # not True → False, not False → True
    assert eval_expr("not True") is False
    assert eval_expr("not False") is True

def test_combined_boolean():
    # not (False or False) and True
    # → (False or False) evaluates to False, not False is True, 그리고 True and True는 True
    expr = "not (False or False) and True"
    assert eval_expr(expr) is True

def test_operator_precedence():
    # 연산자 우선순위 테스트: not이 and보다 우선순위가 높음
    # not True and False → (not True) and False → False and False → False
    expr = "not True and False"
    assert eval_expr(expr) is False

def test_parentheses():
    # 괄호를 통한 우선순위 변경
    # not (True and False) → not False → True
    expr = "not (True and False)"
    assert eval_expr(expr) is True
