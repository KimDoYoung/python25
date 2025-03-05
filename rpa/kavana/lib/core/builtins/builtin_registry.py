from .string_functions import StringFunctions
from .numeric_functions import NumericFunctions

BUILTIN_FUNCTIONS = {
    "LENGTH": (StringFunctions.LENGTH, 1),
    "SUBSTR": (StringFunctions.SUBSTR, 3),
    "UPPER": (StringFunctions.UPPER, 1),
    "LOWER": (StringFunctions.LOWER, 1),
    "TRIM": (StringFunctions.TRIM, 1),
    "LTRIM": (StringFunctions.LTRIM, 1),
    "RTRIM": (StringFunctions.RTRIM, 1),
    "REPLACE": (StringFunctions.REPLACE, 3),
    "SPLIT": (StringFunctions.SPLIT, 2),
    "JOIN": (StringFunctions.JOIN, 2),
    "STARTSWITH": (StringFunctions.STARTSWITH, 2),
    "ENDSWITH": (StringFunctions.ENDSWITH, 2),
    "CONTAINS": (StringFunctions.CONTAINS, 2),
    "INDEX_OF": (StringFunctions.INDEX_OF, 2),

    # ✅ 숫자 관련 함수 추가
    "RANDOM": (NumericFunctions.RANDOM, 2),
}