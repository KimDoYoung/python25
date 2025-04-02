from lib.core.commands.base_command import BaseCommand
from lib.core.datatypes.application import Application
from lib.core.exceptions.kavana_exception import KavanaRpaError
from lib.core.token_type import TokenType
class AppCloseCommand(BaseCommand):
    def execute(self, args, executor):
        ''' APP_CLOSE <app_variable> '''
        if len(args) < 1:
            raise KavanaRpaError("APP_CLOSE 명령어는 최소 하나의 인자가 필요합니다.")

        app_name = args[0].data.string  # ✅ 변수명 가져오기
        app_token = executor.variable_manager.get_variable(app_name)

        if not app_token:
            raise KavanaRpaError(f"변수 '{app_name}'가 정의되지 않았습니다.")

        if app_token.type != TokenType.APPLICATION:
            raise KavanaRpaError(f"변수 '{app_name}'는 Application 타입이 아닙니다.")

        # ✅ 애플리케이션 종료
        try:
            app = app_token.data
            app.close(executor)
            executor.log_command("INFO", f"애플리케이션 {app_name} 종료 완료.")
        except Exception as e:
            raise KavanaRpaError(f"애플리케이션 {app_name} 종료 실패: {str(e)} {app.string}")
