import pytest
from datetime import datetime, timedelta
from lib.core.variable_manager import VariableManager
from lib.core.builtin_functions import BuiltinFunctions
from lib.core.expr_evaluator import ExprEvaluator

def test_basic_arithmetic():
    var_manager = VariableManager()
    assert ExprEvaluator("1 + 2 * 3", var_manager).evaluate() == 7
    assert ExprEvaluator("(1 + 2) * 3", var_manager).evaluate() == 9
    assert ExprEvaluator("10 / 2", var_manager).evaluate() == 5
    assert ExprEvaluator("10 % 3", var_manager).evaluate() == 1

def test_string_operations():
    var_manager = VariableManager()
    assert ExprEvaluator("\"hello\" + \" world\"", var_manager).evaluate() == "hello world"
    assert ExprEvaluator("LENGTH(\"hello\") + 3", var_manager).evaluate() == 8

def test_date_operations():
    var_manager = VariableManager()
    var_manager.set_variable("today", datetime(2025, 2, 20))
    assert ExprEvaluator("today + 3", var_manager).evaluate() == datetime(2025, 2, 23)
    assert ExprEvaluator("today - 3", var_manager).evaluate() == datetime(2025, 2, 17)
    assert ExprEvaluator("today - today", var_manager).evaluate() == 0

def test_builtin_functions():
    var_manager = VariableManager()
    assert ExprEvaluator("LENGTH(\"abcde\")", var_manager).evaluate() == 5
    assert ExprEvaluator("SUBSTR(\"hello\", 1, 3)", var_manager).evaluate() == "ell"
    assert isinstance(ExprEvaluator("CURRENT_DATETIME()", var_manager).evaluate(), datetime)
    assert 1 <= ExprEvaluator("RANDOM(1, 10)", var_manager).evaluate() <= 10

def test_variable_usage():
    var_manager = VariableManager()
    var_manager.set_variable("x", 10)
    var_manager.set_variable("y", 5)
    assert ExprEvaluator("x + y * 2", var_manager).evaluate() == 20
    assert ExprEvaluator("x - y", var_manager).evaluate() == 5

def test_invalid_operations():
    var_manager = VariableManager()
    with pytest.raises(TypeError):
        ExprEvaluator("\"hello\" - \"world\"", var_manager).evaluate()
    with pytest.raises(TypeError):
        ExprEvaluator("10 % 2.5", var_manager).evaluate()
    with pytest.raises(ValueError):
        ExprEvaluator("undefined_var + 3", var_manager).evaluate()

if __name__ == "__main__":
    pytest.main()
