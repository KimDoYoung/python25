from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaFtpError
from lib.core.token import Token


class FtpCommand(BaseCommand):
    ''' 데이터베이스 명령어 해석'''
    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaFtpError("FTP 명령어는 최소 하나 이상의 인자가 필요합니다.")

        sub_command = args[0].data.value.upper()
        options, _ = self.extract_all_options(args, 1)

        option_map = self.get_option_map(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)

        return