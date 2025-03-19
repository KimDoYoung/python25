import time
from lib.core.commands.base_command import BaseCommand
from lib.core.datatypes.image import Image
from lib.core.exceptions.kavana_exception import KavanaSyntaxError
from lib.core.managers.rpa_manager import RPAManager
from lib.core.token_type import TokenType


class WaitCommand(BaseCommand):
    def execute(self, args, executor):
        '''
        WAIT <seconds>  | WAIT image_path [timeout=10]
        '''
        if len(args) < 1:
            executor.raise_command("WAIT 명령어는 최소 하나의 인자가 필요합니다.")

        rpa = RPAManager(executor)  # ✅ 싱글톤 인스턴스 가져오기

        if args[0].type == TokenType.INTEGER:
            seconds = args[0].data.value
            rpa.wait(seconds)  # ✅ RPA 싱글톤에서 실행
            return

        elif args[0].type == TokenType.STRING:  # WAIT "image.png"
            image_path = args[0].data.string
            timeout = 10  # 기본값
            if len(args) > 1 and args[1].type == TokenType.ASSIGN:
                key_token, value_token = args[1].data
                if key_token.data.string.lower() == "timeout" and value_token.type == TokenType.INTEGER:
                    timeout = value_token.data.value

            found_location = rpa.wait_for_image(image.path, timeout)
                
            if found_location is None:
                executor.raise_command(f"이미지 '{image.path}'를 {timeout}초 동안 찾을 수 없습니다.")
            return
        elif args[0].type == TokenType.IMAGE:
            image: Image = args[0].data  # ✅ Image 객체 가져오기

            timeout = 10  # 기본값
            if len(args) > 1 and args[1].type == TokenType.ASSIGN:
                key_token, value_token = args[1].data
                if key_token.data.string.lower() == "timeout" and value_token.type == TokenType.INTEGER:
                    timeout = value_token.data.value

            # ✅ 이미지가 화면에서 발견될 때까지 대기
            found_location = rpa.wait_for_image(image.path, timeout)
            
            if found_location is None:
                executor.raise_command(f"이미지 '{image.path}'를 {timeout}초 동안 찾을 수 없습니다.")

        executor.raise_command("WAIT 명령어의 인자가 올바르지 않습니다.")
