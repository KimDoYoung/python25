import time
import pyautogui
import pyperclip
from lib.core.commands.base_command import BaseCommand
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.managers.rpa_manager import RPAManager


class GetTextCommand(BaseCommand):
    def execute(self, args, executor):
        ''' GET_TEXT '''
        rpa_manager = RPAManager(executor=executor)
        executor.set_last_error("")
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.2)  # 복사 시간 고려
        return pyperclip.paste()