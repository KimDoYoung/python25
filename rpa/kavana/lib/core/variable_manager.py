from lib.core.builtins.builtin_consts import DirectionName, PointName, RegionName
from lib.core.commands.database.db_commander import DbCommander
from lib.core.const_registry import ConstantRegistry
from lib.core.database_registry import DatabaseRegistry
from lib.core.datatypes.kavana_datatype import Integer, String
from lib.core.datatypes.array import Array
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.token import StringToken, Token
from lib.core.token_type import TokenType
class VariableManager:
    """✅ 변수 및 `CONST` 관리"""

    def __init__(self):
        self.global_vars = {}  
        self.local_vars_stack = []
        self.global_vars["_LastError_"] = StringToken(data=String(""), type=TokenType.STRING)
        self.load_built_in_constants()

    def set_variable(self, var_name: str, token: Token, local=False):
        """✅ 변수 설정 (`CONST` 변경 불가)"""
        var_name = var_name.upper()

        # ✅ `CONST` 변경 금지
        if ConstantRegistry.is_constant(var_name):
            raise ValueError(f"CONST {var_name} can not change")

        if local and self.local_vars_stack:
            self.local_vars_stack[-1][var_name] = token
        else:
            self.global_vars[var_name] = token

    def get_variable(self, var_name: str):
        """✅ 변수를 먼저 찾고, 없으면 `CONST`에서 조회"""
        var_name = var_name.upper()

        # ✅ 지역 변수 확인
        if self.local_vars_stack:
            for scope in reversed(self.local_vars_stack):
                if var_name in scope:
                    return scope[var_name]

        # ✅ 전역 변수 확인
        if var_name in self.global_vars:
            return self.global_vars[var_name]

        # ✅ `CONST`에서 조회
        return ConstantRegistry.get(var_name)

    def has_variable(self, var_name: str):
        """✅ 변수 또는 `CONST` 여부 확인"""
        var_name = var_name.upper()
        return (
            any(var_name in scope for scope in self.local_vars_stack) or
            var_name in self.global_vars or
            ConstantRegistry.is_constant(var_name)
        )

    def set_const(self, name: str, value: Token):
        """✅ `CONST` 등록 (한 번만 설정 가능)"""
        name = name.upper()
        ConstantRegistry.define_constant(name, value)

    def load_built_in_constants(self):
        # Enum을 순회하며 상수 등록
        for point_enum in PointName:
            const_name = f"_POINT_{point_enum.name}_"
            self.set_const(
                const_name,
                StringToken(data=String(point_enum.value), type=TokenType.STRING)
            )
        for region_enum in RegionName:
            const_name = f"_REGION_{region_enum.name}_"
            self.set_const(
                const_name,
                StringToken(data=String(region_enum.name), type=TokenType.STRING)
            )
        for direction_enum in DirectionName:
            const_name = f"_DIRECTION_{direction_enum.name}_"
            self.set_const(
                const_name,
                StringToken(data=String(direction_enum.value), type=TokenType.STRING)
            )
    
    def get_db_commander(self, db_name: str) -> DbCommander:
        """✅ DB Commander 가져오기"""
        return DatabaseRegistry.get_commander(db_name)
    
    def set_db_commander(self, db_name: str, commander: DbCommander):
        """✅ DB Commander 설정"""
        db = DatabaseRegistry.get_commander(db_name)
        if db:
            raise KavanaValueError(f"데이터베이스 `{db_name}` 가 이미 존재합니다.")
        DatabaseRegistry.set_commander(db_name, commander)
    