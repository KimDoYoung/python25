from lib.core.builtins.file_dir_functions import FileDirFunctions
from lib.core.builtins.ymd_time_functions import YmdTimeFunctions
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
    "TO_INT" : (StringFunctions.TO_INT, 1),
    "TO_FLOAT" : (StringFunctions.TO_FLOAT, 1),

    # ✅ 숫자 관련 함수 추가
    "RANDOM": (NumericFunctions.RANDOM, 2),
    "ABS": (NumericFunctions.ABS, 1),
    "MAX": (NumericFunctions.MAX, 2),
    "MIN": (NumericFunctions.MIN, 2),
    "ROUND": (NumericFunctions.ROUND, 1),
    "FLOOR": (NumericFunctions.FLOOR, 1),
    "CEIL": (NumericFunctions.CEIL, 1),
    "TRUNC" : (NumericFunctions.TRUNC, 1),
    "IS_EVEN" : (NumericFunctions.IS_EVEN, 1),
    "IS_ODD" : (NumericFunctions.IS_ODD, 1),
    "RANGE" : (NumericFunctions.RANGE, 2),

    # ✅ 날짜 관련 함수 추가
    "YMDTIME": (YmdTimeFunctions.YMDTIME, 6),
    "YMD": (YmdTimeFunctions.YMD, 3),
    "NOW": (YmdTimeFunctions.NOW, 0),
    "TODAY": (YmdTimeFunctions.TODAY, 0),

    # ✅ 파일 관련 함수 추가
    "FILE_READ": (FileDirFunctions.FILE_READ, 1),
    "FILE_WRITE": (FileDirFunctions.FILE_WRITE, 1),
}