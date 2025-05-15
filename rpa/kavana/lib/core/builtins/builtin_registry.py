from lib.core.builtins.datatype_functions import DatatypeFunctions
from lib.core.builtins.dir_functions import DirFunctions
from lib.core.builtins.file_functions import FileFunctions
from lib.core.builtins.path_functions import PathFunctions
from lib.core.builtins.rpa_functions import RpaFunctions
from lib.core.builtins.region_point_functions import RegionPointFunctions
from lib.core.builtins.ymd_time_functions import YmdTimeFunctions
from .string_functions import StringFunctions
from .numeric_functions import NumericFunctions
#TODO builtin함수에 default인자를 줄 수 없나? 인자가 1개 생략되면 default가 적용
#TODO 여러개의 인자를 보낼때, 즉 정해지지 않은 인자갯수 path_join
#TODO " 안에 " 를 처리
BUILTIN_FUNCTIONS = {
    # ✅ 데이터타입관련 함수 추가
    "DUMP_ATTRS": (DatatypeFunctions.DUMP_ATTRS, 1),
    "GET_ATTR": (DatatypeFunctions.GET_ATTR, 2),
    "TYPE_OF": (DatatypeFunctions.TYPE_OF, 1),
    "IS_TYPE": (DatatypeFunctions.IS_TYPE, 2),
    "IS_NULL": (DatatypeFunctions.IS_NULL, 1),
    "IS_NONE": (DatatypeFunctions.IS_NULL, 1), # alias for IS_NULL
    "JSON_STR_PARSE": (DatatypeFunctions.JSON_STR_PARSE, 1),

    # Point Region 관련 함수
    "POINT_OF_REGION": (RegionPointFunctions.POINT_OF_REGION, 2),
    "REGION_OF_REGION": (RegionPointFunctions.REGION_OF_REGION, 2),
    "IS_POINT_IN_REGION": (RegionPointFunctions.IS_POINT_IN_REGION, 2),
    "POINT_MOVE": (RegionPointFunctions.POINT_MOVE, 2),
    "POINT_TO_REGION": (RegionPointFunctions.POINT_TO_REGION, 3),
    "POINTS_TO_REGION": (RegionPointFunctions.POINTS_TO_REGION, 2),
    "REGION_DEVIDE_BY_POINT": (RegionPointFunctions.REGION_DEVIDE_BY_POINT, 2),
    # ✅ RPA 관련 함수 추가
    "WINDOW_LIST":(RpaFunctions.WINDOW_LIST, 1),
    "WINDOW_TOP": (RpaFunctions.WINDOW_TOP, 1),
    "WINDOW_REGION": (RpaFunctions.WINDOW_REGION, 1),
    "WINDOW_FIND_BY_TITLE": (RpaFunctions.WINDOW_FIND_BY_TITLE, 1),
    "MONITOR_LIST": (RpaFunctions.MONITOR_LIST, 0),
    "SNAP_SCREEN_HASH": (RpaFunctions.SNAP_SCREEN_HASH, 2),
    "SNAP_CHANGED_REGION": (RpaFunctions.SNAP_CHANGED_REGION, 2),
    "PROCESS_LIST": (RpaFunctions.PROCESS_LIST, 0),
    "PROCESS_IS_RUNNING": (RpaFunctions.PROCESS_IS_RUNNING, 1),
    "PROCESS_KILL": (RpaFunctions.PROCESS_KILL, 1),
    "PROCESS_FOCUS": (RpaFunctions.PROCESS_FOCUS, 1),

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
    "TO_STR" : (StringFunctions.TO_STR, 1),
    "REG_EX" : (StringFunctions.REG_EX, 2),
    "MAKE_SQL" : (StringFunctions.MAKE_SQL, 2),

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
    "POWER" : (NumericFunctions.POWER, 2),
    "SQRT" : (NumericFunctions.SQRT, 1),
    "SIN" : (NumericFunctions.SIN, 1),
    "COS" : (NumericFunctions.COS, 1),
    "TAN" : (NumericFunctions.TAN, 1),
    "MOD" : (NumericFunctions.MOD, 2),

    # ✅ 날짜 관련 함수 추가
    "YMDTIME": (YmdTimeFunctions.YMDTIME, 6),
    "YMD": (YmdTimeFunctions.YMD, 3),
    "NOW": (YmdTimeFunctions.NOW, 0),
    "TODAY": (YmdTimeFunctions.TODAY, 0),
    "WEEKDAY": (YmdTimeFunctions.WEEKDAY, 1),
    "IS_WEEKEND": (YmdTimeFunctions.IS_WEEKEND, 1),
    "WEEK_NAME": (YmdTimeFunctions.WEEK_NAME, 2),
    "YMD_FORMAT": (YmdTimeFunctions.YMD_FORMAT, 2),

    # ✅ 파일 관련 함수 추가
    "FILE_READ": (FileFunctions.FILE_READ, 1),
    "FILE_WRITE": (FileFunctions.FILE_WRITE, 1),
    "FILE_APPEND": (FileFunctions.FILE_APPEND, 1),
    "FILE_EXISTS": (FileFunctions.FILE_EXISTS, 1),
    "FILE_DELETE": (FileFunctions.FILE_DELETE, 1),
    "FILE_INFO" : (FileFunctions.FILE_INFO, 1),
    "FILE_COPY" : (FileFunctions.FILE_COPY, 2),
    "FILE_MOVE" : (FileFunctions.FILE_MOVE, 2),
    "FILE_HASH" : (FileFunctions.FILE_HASH, 2),
    "FILE_LINES" : (FileFunctions.FILE_LINES, 1),
    "FILE_FIND" : (FileFunctions.FILE_FIND, 2),
    "FILE_TEMP_NAME" : (FileFunctions.FILE_TEMP_NAME, 1),
    
    # ✅ PATH 관련 함수 추가
    "PATH_JOIN": (PathFunctions.PATH_JOIN, 2),
    "PATH_BASENAME": (PathFunctions.PATH_BASENAME, 1),
    "PATH_DIRNAME": (PathFunctions.PATH_DIRNAME, 1),

    # ✅ 디렉토리 관련 함수 추가
    "DIR": (DirFunctions.DIR, 1),
    "DIR_LIST": (DirFunctions.DIR_LIST, 1),
    "DIR_EXISTS": (DirFunctions.DIR_EXISTS, 1),
    "DIR_CREATE": (DirFunctions.DIR_CREATE, 1),
    "DIR_DELETE": (DirFunctions.DIR_DELETE, 1),
    "DIR_RENAME": (DirFunctions.DIR_RENAME, 2),
}