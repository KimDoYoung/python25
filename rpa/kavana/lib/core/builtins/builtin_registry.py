from lib.core.builtins.datatype_functions import DatatypeFunctions
from lib.core.builtins.dir_functions import DirFunctions
from lib.core.builtins.file_functions import FileFunctions
from lib.core.builtins.path_functions import PathFunctions
from lib.core.builtins.ymd_time_functions import YmdTimeFunctions
from .string_functions import StringFunctions
from .numeric_functions import NumericFunctions

BUILTIN_FUNCTIONS = {
    # ✅ 데이터타입관련 함수 추가
    "TYPE_OF": (DatatypeFunctions.TYPE_OF, 1),
    "IS_TYPE": (DatatypeFunctions.IS_TYPE, 2),
    "IS_NULL": (DatatypeFunctions.IS_NULL, 1),
    "IS_NONE": (DatatypeFunctions.IS_NULL, 1), # alias for IS_NULL
    "JSON_STR_PARSE": (DatatypeFunctions.JSON_STR_PARSE, 1),
    # ✅ 문자열 관련 함수 추가
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
    "FILE_READ": (FileFunctions.FILE_READ, 1),
    "FILE_WRITE": (FileFunctions.FILE_WRITE, 1),
    "FILE_APPEND": (FileFunctions.FILE_APPEND, 1),
    "FILE_EXISTS": (FileFunctions.FILE_EXISTS, 1),
    "FILE_DELETE": (FileFunctions.FILE_DELETE, 1),
    "FILE_SIZE": (FileFunctions.FILE_SIZE, 1),
    "FILE_MODIFIED_TIME": (FileFunctions.FILE_MODIFIED_TIME, 1),
    "FILE_TYPE" : (FileFunctions.FILE_TYPE, 1),
    "FILE_COPY" : (FileFunctions.FILE_COPY, 2),
    "FILE_MOVE" : (FileFunctions.FILE_MOVE, 2),
    "FILE_HASH" : (FileFunctions.FILE_HASH, 2),
    "FILE_LINES" : (FileFunctions.FILE_LINES, 1),
    "FILE_FIND" : (FileFunctions.FILE_FIND, 2),
    
    # ✅ PATH 관련 함수 추가
    "PATH_JOIN": (PathFunctions.PATH_JOIN, 2),
    "PATH_BASENAME": (PathFunctions.PATH_BASENAME, 1),
    "PATH_DIRNAME": (PathFunctions.PATH_DIRNAME, 1),

    # ✅ 디렉토리 관련 함수 추가
    "DIR_LIST": (DirFunctions.DIR_LIST, 1),
    "DIR_EXISTS": (DirFunctions.DIR_EXISTS, 1),
    "DIR_CREATE": (DirFunctions.DIR_CREATE, 1),
    "DIR_DELETE": (DirFunctions.DIR_DELETE, 1),
}