from lib.core.commands.base_command import BaseCommand
from lib.core.datatypes.application import Application

class CloseChildWindowsCommand(BaseCommand):
    def execute(self, args, executor):
        """CLOSE_CHILD_WINDOWS <app_variable>"""
        if len(args) < 1:
            executor.raise_command("CLOSE_CHILD_WINDOWS 명령어는 최소 하나의 인자가 필요합니다.")

        app_name = args[0].data.string  # ✅ 변수명 가져오기
        app = executor.variable_manager.get_variable(app_name)

        if not app:
            executor.raise_command(f"변수 '{app_name}'가 정의되지 않았습니다.")

        if not isinstance(app, Application):
            executor.raise_command(f"변수 '{app_name}'는 Application 타입이 아닙니다.")

        # ✅ 애플리케이션 자식 윈도우 닫기
        try:
            app.close_child_windows(executor)
            executor.log_command("INFO", f"애플리케이션 {app_name}의 모든 자식 윈도우 닫기 완료.")
        except Exception as e:
            executor.raise_command(f"애플리케이션 {app_name}의 자식 윈도우 닫기 실패: {str(e)}")
