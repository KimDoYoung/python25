class CommandExecutor:
    """
    CommandExecutor는 Kavana 스크립트에서 파싱된 명령을 실행한다.
    """
    def __init__(self):
        pass

    def execute(self, command: dict):
        """
        주어진 명령을 실행한다.
        :param command: {"cmd": "PRINT", "args": ["hello"]}
        """
        cmd = command["cmd"]
        args = command["args"]

        if cmd == "PRINT":
            self._execute_print(args)
        elif cmd == "PRINTLN":
            self._execute_println(args)
        else:
            raise ValueError(f"Unknown command: {cmd}")

    def _execute_print(self, args):
        """
        PRINT 명령어 실행 (출력)
        예: PRINT("Hello, World!")
        """
        if not args:
            raise SyntaxError("PRINT command requires at least one argument.")

        output = args[0]  # 첫 번째 인자를 가져오기
        if output.startswith('"') and output.endswith('"'):
            output = output[1:-1]  # 따옴표 제거

        print(output)

    def _execute_println(self, args):
        """
        PRINTLN 명령어 실행 (출력 후 개행)
        예: PRINTLN("Hello, World!")
        """
        if not args:
            print()  # ✅ 인자가 없으면 개행만 출력
        else:
            output = " ".join(args)  # ✅ 여러 인자가 있을 경우 공백으로 결합
            if output.startswith('"') and output.endswith('"'):
                output = output[1:-1]  # ✅ 따옴표 제거
            print(output)  # ✅ 기본 출력 (자동 개행 포함)
