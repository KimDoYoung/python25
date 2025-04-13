from lib.core.commands.base_command import BaseCommand
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.managers.rpa_manager import RpaManager


class PutTextCommand(BaseCommand):
    '''
    PUT_TEXT <express:string>
    '''
    def execute(self, args, executor):
        rpa_manager = RpaManager(executor=executor)
        executor.set_last_error("")
        express, i = self.extract_option1(args, 0)
        str=ExprEvaluator(executor=executor).evaluate(express).data.value
        rpa_manager.put_text(str)
        return