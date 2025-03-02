class BreakException(Exception):
    """반복문을 종료하는 예외"""
    pass

class ContinueException(Exception):
    """반복문의 현재 실행을 건너뛰는 예외"""
    pass

class TokenizationError(Exception):
    """토큰화 과정에서 발생하는 오류"""
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        error_location = f" at line {line}, column {column}" if line is not None and column is not None else ""
        super().__init__(f"TokenizationError: {message}{error_location}")


class DataTypeError(Exception):
    """데이터 타입 변환 오류"""
    def __init__(self, message, value=None):
        self.message = message
        self.value = value
        error_value = f" (value: {value})" if value is not None else ""
        super().__init__(f"DataTypeError: {message}{error_value}")

class ExprEvaluationError(Exception):
    """표현식 평가 오류"""
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        error_location = f" at line {line}, column {column}" if line is not None and column is not None else ""
        super().__init__(f"ExprEvaluationError: {message}{error_location}")

class CommandExecutionError(Exception):
    """명령어 실행 오류"""
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        error_location = f" at line {line}, column {column}" if line is not None and column is not None else ""
        
        super().__init__(f"CommandExecutionError: {message}{error_location}")