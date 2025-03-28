from lib.core.commands.base_command import BaseCommand
from lib.core.commands.database.db_commander import DbCommander
from lib.core.commands.database.maria_db_commander import MariaDbCommander
from lib.core.commands.database.postgresql_db_commander import PostgreDbCommander
from lib.core.commands.database.sqlite_db_commander import SqliteDbCommander
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.expr_evaluator import ExprEvaluator


class DatabaseCommand(BaseCommand):
    ''' 데이터베이스 명령어 해석'''
    def execute(self, args, executor):
        self.executor = executor
        if len(args) < 1:
            return
        sub_command = args[0].upper() 
        options, i = self.extract_all_options(args, 1)
        db_type = options.get("type", "sqlite")
        db_name = options.get("name", "default")
        # create DbCommander with type
        db_commander = self.new_db_commander(db_type)
        executor.set_db_commander(db_name, db_commander)
        db_arg = {}
        for option in options:
            key = option.lower()
            express = options[option]
            value = ExprEvaluator(executor=executor).evaluate(express).data.value
            db_arg[key] = value
        db_commander.connect(**db_arg)
        return

    def new_db_commander(db_type:str)->DbCommander:
        ''' 데이터베이스 명령어 생성'''

        if db_type == "sqlite":
            return SqliteDbCommander()
        elif db_type == "mariadb":
            return MariaDbCommander()
        elif db_type == "postgresql":
            return PostgreDbCommander()
        else:
            raise KavanaValueError(f"지원하지 않는 데이터베이스입니다.(지원:`sqlite`,`postgresql`,`mariadb`): {db_type}")