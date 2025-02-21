from lib.core.commands.base_command import BaseCommand

class PrintCommand(BaseCommand):
    def execute(self, args, executor):
        if not args:
            raise SyntaxError("PRINT command requires at least one argument.")

        # ✅ 여러 인자를 공백으로 결합
        output = " ".join(args)

        # ✅ 따옴표 제거 (예: PRINT "Hello" → Hello)
        if output.startswith('"') and output.endswith('"'):
            output = output[1:-1]

        # ✅ 특수 문자(\n, \t) 지원
        output = output.replace("\\n", "\n").replace("\\t", "\t")

        print(output)