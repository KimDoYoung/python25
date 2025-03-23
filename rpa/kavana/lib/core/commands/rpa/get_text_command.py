from contextvars import Token
import time
from tokenize import String
import pyautogui
import pyperclip
from lib.core.commands.base_command import BaseCommand
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.managers.rpa_manager import RPAManager
from lib.core.token_type import TokenType


class GetTextCommand(BaseCommand):
    def execute(self, args, executor):
        ''' GET_TEXT var_to=var_name :text를 var_name에 저장합니다 '''

        rpa_manager = RPAManager(executor=executor)
        executor.set_last_error("")
        rpa_manager.key_in(["ctrl+a", "ctrl+c"])
        time.sleep(0.2)  # 복사 시간 고려
        var_name=""
        if (len(args) == 3 
            and args[0].data.string.upper() == "VAR_TO"
            and args[1].type == TokenType.ASSIGN
            and args[2].type == TokenType.IDENTIFIER):
            var_name = args[2].data.string
            text = pyperclip.paste()
            result_token = Token(data=String(text), type=TokenType.STRING)
            executor.set_variable(var_name, result_token)
            return
        else:
            executor.set_last_error("문법: GET_TEXT INTO var_name :text를 var_name에 저장합니다")
        return 