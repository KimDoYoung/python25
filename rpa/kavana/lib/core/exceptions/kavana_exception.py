class KavanaException(Exception):
    """Kavana 스크립트에서 발생하는 모든 예외의 기본 클래스"""
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        error_location = f" at line {line}, column {column}" if line is not None and column is not None else ""
        super().__init__(f"{self.__class__.__name__}: {message}{error_location}")

# ✅ 기존 예외를 `KavanaException`에서 상속받도록 변경

class BreakException(KavanaException):
    """반복문을 종료하는 예외"""
    pass

class ContinueException(KavanaException):
    """반복문의 현재 실행을 건너뛰는 예외"""
    pass

class DataTypeError(KavanaException):
    """데이터 타입 변환 오류"""
    pass

class ExprEvaluationError(KavanaException):
    """표현식 평가 오류"""
    pass


class CommandExecutionError(KavanaException):
    """명령어 실행 오류"""
    pass

class CommandParserError(KavanaException):
    """명령어 파싱 오류"""
    pass

class FunctionParserError(KavanaException):
    """함수 파싱 오류"""
    pass

class CustomTokenMakerError(KavanaException):
    """토큰 생성 오류"""
    pass

class KavanaSyntaxError(KavanaException):
    """구문 오류"""
    pass

class KavanaValueError(KavanaException):
    """값 오류"""
    pass

class KavanaTypeError(KavanaException):
    """값 오류"""
    pass

class KavanaFileNotFoundError(KavanaException):
    """파일이 존재하지 않는 경우"""
    pass

class KavanaIndexError(KavanaException):
    """인덱스 오류"""
    pass

class KavanaKeyError(KavanaException):
    """키 오류"""
    pass

class KavanaDatabaseError(KavanaException):
    """데이터베이스 오류"""
    pass

class KavanaRpaError(KavanaException):
    """RPA 관련 오류"""
    pass
class KavanaFtpError(KavanaException):
    """FTP 관련 오류"""
    pass
class KavanaSftpError(KavanaException):
    """SFTP 관련 오류"""
    pass
class KavanaHttpError(KavanaException):
    """HTTP 관련 오류"""
    pass
class KavanaImageError(KavanaException):
    """Image 관련 오류"""
    pass
class KavanaOcrError(KavanaException):
    """Ocr 관련 오류"""
    pass
class KavanaBrowserError(KavanaException):
    """Browser 관련 오류"""
    pass

class KavanaHtmlError(KavanaException):
    """HTML 관련 오류"""
    pass
