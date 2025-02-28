from lib.core.expr_evaluator import ExprEvaluator
from lib.core.function_parser import FunctionParser
from lib.core.function_registry import FunctionRegistry

test_cases = [
    "MY_FUNC(3,4)",
    "MY_FUNC()",
    "MY_FUNC((3),(4))",
    "MY_FUNC(LENGTH(\"abc\"),4)",
    "MY_FUNC(SUBSTR(\"123\",1,2),4)",
    "MY_FUNC(42)",
    "MY_FUNC(1,2,3)"
]

expr = ExprEvaluator("1 + 2", None)
for case in test_cases:
    print(expr.split_function_token(case))
