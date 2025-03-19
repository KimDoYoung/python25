from lib.core.commands.base_command import BaseCommand


class AppOpenCommand(BaseCommand):
    def execute(self, args, executor):
        # if len(args) < 1:
        #     raise SyntaxError("APP_OPEN 명령어는 최소 하나의 인자가 필요합니다.")

        # app_name = args[0].data.string
        # app = executor.variable_manager.get_variable(app_name)

        # if not app:
        #     raise NameError(f"변수 '{app_name}'가 정의되지 않았습니다.")

        # # 애플리케이션 열기
        # app.open()
        # if len(args) > 1:
        #     for arg in args[1:]:
        #         if arg.type == TokenType.KEYWORD:
        #             if arg.data.string == "maximize":
        #                 app.maximize()
        #             elif arg.data.string == "minimize":
        #                 app.minimize()
        #             elif arg.data.string == "restore":
        #                 app.restore()
        #             elif arg.data.string == "close":
        #                 app.close()
        #             else:
        #                 raise SyntaxError(f"올바르지 않은 키워드 '{arg.data.string}'입니다.")
        #         else:
        #             raise SyntaxError("키워드가 필요합니다.")
        return