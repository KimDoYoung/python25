from lib.core.commands.base_command import BaseCommand
from lib.core.commands.database.db_commander import DbCommander
from lib.core.commands.database.maria_db_commander import MariaDbCommander
from lib.core.commands.database.postgresql_db_commander import PostgreDbCommander
from lib.core.commands.database.sqlite_db_commander import SqliteDbCommander
from lib.core.datatypes.hash_map import HashMap
from lib.core.exceptions.kavana_exception import KavanaDatabaseError, KavanaValueError
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import ArrayToken, HashMapToken, Token, TokenStatus
from lib.core.token_type import TokenType
from lib.core.datatypes.array import Array
from lib.core.token_util import TokenUtil

class DatabaseCommand(BaseCommand):
    ''' 데이터베이스 명령어 해석'''
    OPTION_DEFINITIONS = {
        "type": {"default": "sqlite", "allowed_types": [TokenType.STRING]},
        "name": {"default": "default", "allowed_types": [TokenType.STRING]},
        "path": {"required": True, "allowed_types": [TokenType.STRING]},
        "url": {"required": True, "allowed_types": [TokenType.STRING]},
        "sql": {"required": True, "allowed_types": [TokenType.STRING]},
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
    }

    COMMAND_SPECS = {
        "connect": {
            "keys": ["path", "url"],
            "overrides": {
                "path": {"required": True},
                "url": {"required": True}
            },
            "rules": {
                "mutually_exclusive": [],
                "required_together": []
            }
        },
        "execute": {
            "keys": ["sql"],
            "overrides": {
                "sql": {"required": True}
            },
            "rules": {
                "mutually_exclusive": [],
                "required_together": []
            }
        },
        "query": {
            "keys": ["sql", "to_var"],
            "overrides": {
                "sql": {"required": True},
                "to_var": {"required": False}
            },
            "rules": {
                "mutually_exclusive": [],
                "required_together": []
            }
        },
        "close": {
            "keys": [],
            "overrides": {},
            "rules": {
                "mutually_exclusive": [],
                "required_together": []
            }
        },
        "begin_transaction": {
            "keys": [],
            "overrides": {},
            "rules": {
                "mutually_exclusive": [],
                "required_together": []
            }
        },
        "commit": {
            "keys": [],
            "overrides": {},
            "rules": {
                "mutually_exclusive": [],
                "required_together": []
            }
        },
        "rollback": {
            "keys": [],
            "overrides": {},
            "rules": {
                "mutually_exclusive": [],
                "required_together": []
            }
        }
    }


    def execute(self, args: list[Token], executor):
        self.executor = executor
        if not args:
            raise KavanaDatabaseError("DB 명령어는 최소 하나 이상의 인자가 필요합니다.")

        sub_command = args[0].data.value.upper()
        options, _ = self.extract_all_options(args, 1)

        db_type = self._get_option_value(options, "type", executor, default="sqlite")
        db_name = self._get_option_value(options, "name", executor, default="default")

        option_map = self.get_option_map(db_type, sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)

        try:
            if sub_command == "CONNECT":
                executor.log_command("INFO", f"{db_type} {db_name} 데이터베이스 연결")
                self._connect_db(db_type, db_name, option_values, executor)

            elif sub_command in ("EXECUTE", "QUERY", "CLOSE", "BEGIN_TRANSACTION", "COMMIT", "ROLLBACK"):
                db_commander = self._get_db_commander_or_raise(db_name, executor)

                match sub_command:
                    case "EXECUTE":
                        executor.log_command("INFO", f"{db_name} : Execute 수행 sql : [{option_values["sql"]}]")
                        db_commander.execute(option_values["sql"])
                    case "QUERY":
                        executor.log_command("INFO", f"{db_name} : Query 수행  sql : [{option_values["sql"]}]")
                        result = db_commander.query(option_values["sql"])
                        if "to_var" in option_values:
                            self._store_query_result(result, option_values["to_var"], executor)
                    case "CLOSE":
                        executor.log_command("INFO", f"{db_name} 데이터베이스 연결 종료")
                        db_commander.close()
                    case "BEGIN_TRANSACTION":
                        executor.log_command("INFO", f"{db_name} 데이터베이스 트랜잭션 시작")
                        db_commander.begin_transaction()
                    case "COMMIT":
                        executor.log_command("INFO", f"{db_name} COMMIT")
                        db_commander.commit()
                    case "ROLLBACK":
                        executor.log_command("INFO", f"{db_name} ROLLBACK")
                        db_commander.rollback()
            else:
                raise KavanaDatabaseError(f"`{sub_command}` 지원하지 않는 데이터베이스 명령어입니다.")

        except Exception as e:
            raise KavanaDatabaseError(f"`{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e


    def new_db_commander(self, db_type:str)->DbCommander:
        ''' 데이터베이스 명령어 생성'''

        if db_type == "sqlite":
            return SqliteDbCommander()
        elif db_type == "mariadb":
            return MariaDbCommander()
        elif db_type == "postgresql":
            return PostgreDbCommander()
        else:
            raise KavanaDatabaseError(f"지원하지 않는 데이터베이스입니다.(지원:`sqlite`,`postgresql`,`mariadb`): {db_type}")
        

    # 필요한 키만 추려서 option_map 구성
    def option_map_define(self, *keys):
        option_map = {}
        if 'type' not in keys:
            option_map["type"] = self.OPTION_DEFINITIONS["type"]
        if 'name' not in keys:
            option_map["name"] = self.OPTION_DEFINITIONS["name"]
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
            
            case ("sqlite", "CLOSE") | ("postgres", "CLOSE") | ("mariadb", "CLOSE"):
                return self.option_map_define()
            
            case ("sqlite", "BEGIN_TRANSACTION") | ("postgres", "BEGIN_TRANSACTION") | ("mariadb", "BEGIN_TRANSACTION"):
                return self.option_map_define()

            case ("sqlite", "COMMIT") | ("postgres", "COMMIT") | ("mariadb", "COMMIT"):
                return self.option_map_define()

            case ("sqlite", "ROLLBACK") | ("postgres", "ROLLBACK") | ("mariadb", "ROLLBACK"):
                return self.option_map_define()

            case _:
                raise KavanaDatabaseError(f"지원하지 않는 db_type 또는 sub_command: {db_type}, {sub_command}")

    # =========================
    # 🔽 헬퍼 메서드들
    # =========================

    def _get_option_value(self, options, key, executor, default=None):
        option = options.get(key)
        if option:
            expr = option['express']
            return ExprEvaluator(executor=executor).evaluate(expr).data.value
        return default

    def _get_db_commander_or_raise(self, db_name, executor):
        db_commander = executor.get_db_commander(db_name)
        if db_commander is None:
            raise KavanaDatabaseError(f"연결된 데이터베이스가 없습니다. {db_name}")
        return db_commander

    def _connect_db(self, db_type, db_name, option_values, executor):
        db_commander = self.new_db_commander(db_type)
        executor.set_db_commander(db_name, db_commander)  # 이미 존재하면 exception 발생
        db_commander.connect(**option_values)

    def _store_query_result(self, result, to_var, executor):
        result_array = []
        for row in result:
            converted = {k: v for k, v in row.items()}
            row_token = TokenUtil.dict_to_hashmap_token(converted)
            result_array.append(row_token)
        result_token = TokenUtil.array_to_array_token(result_array)
        executor.set_variable(to_var, result_token)