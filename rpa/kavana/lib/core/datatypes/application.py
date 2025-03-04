from lib.core.datatypes.kavana_datatype import KavanaDataType

class Application(KavanaDataType):
    def __init__(self, name: str):
        self.name = name
        self.value = name  # ✅ value를 name으로 설정

    def __str__(self):
        return f"Application(name={self.name})"

    @property
    def string(self):
        """애플리케이션 이름을 문자열로 변환"""
        return self.name

    @property
    def primitive(self):
        """Python 기본 타입 변환 (애플리케이션은 이름 문자열로 변환)"""
        return self.name
