from lib.core.commands.base_command import BaseCommand
from lib.core.commands.database.db_commander import DbCommander
from lib.core.commands.database.maria_db_commander import MariaDbCommander
from lib.core.commands.database.postgresql_db_commander import PostgreDbCommander
from lib.core.commands.database.sqlite_db_commander import SqliteDbCommander
from lib.core.datatypes.hash_map import HashMap
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import ArrayToken
from lib.core.token_type import TokenType
from lib.core.datatypes.array import Array
from lib.core.token_util import TokenUtil

class DatabaseCommand(BaseCommand):
    ''' 데이터베이스 명령어 해석'''
    def execute(self, args, executor):
        self.executor = executor
        if len(args) < 1:
            return
        sub_command = args[0].data.value.upper() 
        options, i = self.extract_all_options(args, 1)

        type_express = options.get("type")
        if type_express:
            db_type = ExprEvaluator(executor=executor).evaluate(type_express).data.value
        else:
            db_type = "sqlite"

        dbname_express = options.get("name")
        if dbname_express:
            db_name = ExprEvaluator(executor=executor).evaluate(dbname_express).data.value
        else:
            db_name = "default"

        option_map = self.get_option_map(db_type, sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)

        if sub_command == "CONNECT":    
            db_commander = self.new_db_commander(db_type)
            executor.set_db_commander(db_name, db_commander) # 이미 존재하면 exception 발생
            db_commander.connect(**option_values)
        elif sub_command == "EXECUTE":
            db_commander = executor.get_db_commander(db_name)
            if db_commander is None:
                raise KavanaValueError(f"연결된 데이터베이스가 없습니다. {db_name}")
            db_commander.execute(**option_values)
        elif sub_command == "QUERY":
            db_commander = executor.get_db_commander(db_name)
            if db_commander is None:
                raise KavanaValueError(f"연결된 데이터베이스가 없습니다. {db_name}")
            sql = option_values["sql"]
            result = db_commander.query(sql)
        
            if "to_var" in option_values:
                to_var = option_values["to_var"]
                result_array = Array()  # 빈 배열 생성

                for row in result:  # row: Dict[str, Any]
                    # Python dict → Kavana HashMap
                    converted = {
                        k: TokenUtil.primitive_to_kavana(v) for k, v in row.items()
                    }
                    row_map = HashMap(value=converted)
                    result_array.append(row_map)
                result_array_token = ArrayToken(result_array)
                result_array_token.element_type = TokenType.HASH_MAP
                result_array_token.type = TokenType.ARRAY
                executor.set_variable(to_var, result_array_token)
        else:
            raise KavanaValueError(f"지원하지 않는 데이터베이스 명령어입니다: {sub_command}")
        return

    def new_db_commander(self, db_type:str)->DbCommander:
        ''' 데이터베이스 명령어 생성'''

        if db_type == "sqlite":
            return SqliteDbCommander()
        elif db_type == "mariadb":
            return MariaDbCommander()
        elif db_type == "postgresql":
            return PostgreDbCommander()
        else:
            raise KavanaValueError(f"지원하지 않는 데이터베이스입니다.(지원:`sqlite`,`postgresql`,`mariadb`): {db_type}")
        
    OPTION_DEFINITIONS = {
        # "type": {"default": "sqlite", "allowed_types": [TokenType.STRING]},
        # "name": {"default": "default", "allowed_types": [TokenType.STRING]},
        "path": {"required": True, "allowed_types": [TokenType.STRING]},
        "url": {"required": True, "allowed_types": [TokenType.STRING]},
        "sql": {"required": True, "allowed_types": [TokenType.STRING]},
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
    }
    # 필요한 키만 추려서 option_map 구성
    def option_map_define(self, *keys):
        option_map = {}
        # option_map["type"] = self.OPTION_DEFINITIONS["type"]
        # option_map["name"] = self.OPTION_DEFINITIONS["name"]
        for key in keys:
            option_map[key] = self.OPTION_DEFINITIONS[key]
        return option_map    
        
    def get_option_map(self, db_type: str, sub_command: str) -> dict:
        '''db_type과 sub_command 조합별 옵션 맵 생성'''
        match (db_type, sub_command):
            case ("sqlite", "CONNECT"):
                return self.option_map_define("path")
            case ("postgres", "CONNECT") | ("mariadb", "CONNECT"):
                return self.option_map_define("url")
            
            case ("sqlite", "EXECUTE") | ("postgres", "EXECUTE") | ("mariadb", "EXECUTE"):
                return self.option_map_define("sql")

            case ("sqlite", "QUERY") | ("postgres", "QUERY") | ("mariadb", "QUERY"):
                return self.option_map_define("sql", "to_var")

            case _:
                raise KavanaValueError(f"지원하지 않는 db_type 또는 sub_command: {db_type}, {sub_command}")
