from lib.core.commands.base_command import BaseCommand

class ExitCommand(BaseCommand):
    def execute(self, args, executor):
        exit()  # ✅ 프로그램 종료