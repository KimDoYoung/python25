import re
from lib.core.datatypes.kavana_datatype import KavanaDataType
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.logger import Logger
from lib.core.commands.base_command import BaseCommand
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.command_preprocessor import CommandPreprocessor
from lib.core.command_parser import CommandParser
from lib.core.token_util import TokenUtil

class BaseLogCommand(BaseCommand):
    """로그 출력 명령어의 기본 클래스 (공통 로직 포함)"""

    def log(self, level: str, args: list[Token], executor):
        if not args:
            raise ValueError(f"{level} 명령어는 최소 하나의 인자가 필요합니다. (예: {level} '메시지')")

        # ✅ 여러 인자를 공백으로 결합하여 문자열 생성
        raw_message = " ".join(token.data.string for token in args)
        message = self._evaluate_message(raw_message, executor)

        # ✅ 로그 출력
        logger = Logger()
        log_method = getattr(logger, level.lower())  # INFO, DEBUG, WARN, ERROR 동적으로 호출
        log_method(message)

    def _evaluate_message(self, message: str, executor):
        """문자열 내 `{}` 표현식을 평가하여 실제 값으로 변환"""
        def replace_expr(match):
            expression = match.group(1)  # `{}` 내부 표현식
            
            try:
                # ✅ 문자열을 토큰화하여 ExprEvaluator에 전달
                ppLines = CommandPreprocessor().preprocess([expression])
                tokens = CommandParser.tokenize(ppLines[0])
                evaluator = ExprEvaluator(executor)
                
                # ✅ 평가 후 문자열 반환
                result_token = evaluator.evaluate(tokens)
                if isinstance(result_token, Token):
                    return(result_token.data.string)
                elif isinstance(result_token, KavanaDataType):
                    return result_token.string
                else:
                    raise KavanaValueError(f"지원되지 않는 타입: {type(result_token)}", match.start(), match.end())
                #return str(result_token.data.string) if isinstance(result_token, Token) else str(result_token.string)                                    
                # return str(result_token.data.value) if isinstance(result_token, Token) else str(result_token.string)
            except Exception as e:
                return f"{{ERROR: {e}}}"  # 오류 발생 시 그대로 출력

        # ✅ `{}` 패턴을 찾아 `ExprEvaluator`를 사용하여 해석
        return re.sub(r"\{(.*?)\}", replace_expr, message)

class LogInfoCommand(BaseLogCommand):
    """LOG_INFO "message" -> INFO 로그 출력"""

    def execute(self, args: list[Token], executor):
        self.log("INFO", args, executor)

class LogDebugCommand(BaseLogCommand):
    """LOG_DEBUG "message" -> DEBUG 로그 출력"""

    def execute(self, args: list[Token], executor):
        self.log("DEBUG", args, executor)

class LogWarnCommand(BaseLogCommand):
    """LOG_WARN "message" -> WARN 로그 출력"""

    def execute(self, args: list[Token], executor):
        self.log("WARN", args, executor)

class LogErrorCommand(BaseLogCommand):
    """LOG_ERROR "message" -> ERROR 로그 출력"""

    def execute(self, args: list[Token], executor):
        self.log("ERROR", args, executor)


class LogConfigCommand(BaseCommand):
    """LOG_CONFIG dir=<express:string>, prefix=<express:string>, level=<express:string>"""

    def execute(self, args: list[Token], executor):
        logger = Logger()  # ✅ Logger 인스턴스 가져오기
        config_params = {"dir": None, "prefix": None, "level": None} # 인자 들

        if not args:
            # ✅ 현재 로그 설정 출력
            print(f"현재 로그 설정: dir='{logger.log_dir}', prefix='{logger.log_prefix}', level='{logger.logger.level}'")
            return

        i = 0
        while i < len(args):
            # ✅ `find_key_value()`를 사용하여 key, value 토큰 추출
            key_token, value_tokens, i = TokenUtil.find_key_value(args, i)

            if key_token is None or not value_tokens:
                raise KavanaValueError("LOG_CONFIG 명령어의 인자는 `key=\"value\"` 형태여야 합니다.", key_token.line, key_token.column)

            # ✅ `=` 연산자 확인
            if value_tokens[0].type != TokenType.ASSIGN:
                raise KavanaValueError(f"잘못된 형식: `{key_token.data.string}` 다음에는 `=`가 와야 합니다.", key_token.line, key_token.column)

            key = key_token.data.string.lower()
            if key not in config_params:
                raise KavanaValueError(f"지원되지 않는 로그 설정 키: `{key}` (가능한 값: dir, prefix, level)", key_token.line, key_token.column)

            # ✅ `=` 이후의 표현식만 추출하여 평가
            expr_tokens = value_tokens[1:]  # `=` 연산자 제거
            if not expr_tokens:
                raise KavanaValueError(f"로그 설정 `{key}`의 값이 비어 있습니다.", key_token.line, key_token.column)
            config_params[key] = expr_tokens

        # 담은 것을 해석    
        evaluator = ExprEvaluator(executor)
        for key, expr_tokens in config_params.items():    
            try:
                if not expr_tokens:
                    continue
                evakyated_token = evaluator.evaluate(expr_tokens)  # ✅ 표현식 평가
                value = evakyated_token.data.string  # ✅ 평가된 값을 문자열로 변환
                config_params[key] = value
            except Exception as e:
                raise KavanaValueError(f"로그 설정 `{key}`의 값 평가 오류: {e}", key_token.line, key_token.column)

        # ✅ 설정 적용 (None이면 기존 값 유지)
        logger.set_config(
            log_dir=config_params["dir"] if config_params["dir"] else logger.log_dir,
            log_prefix=config_params["prefix"] if config_params["prefix"] else logger.log_prefix,
            log_level=config_params["level"] if config_params["level"] else logger.log_level
        )

        # ✅ 변경 사항 출력
        #print(f"✅ 로그 설정 변경됨: dir='{logger.log_dir}', prefix='{logger.log_prefix}', level='{logger.logger.level}'")

