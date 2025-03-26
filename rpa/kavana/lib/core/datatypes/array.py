from lib.core.datatypes.kavana_datatype import KavanaDataType
from lib.core.exceptions.kavana_exception import KavanaIndexError, KavanaTypeError, KavanaValueError


class Array(KavanaDataType):
    def __init__(self, *values):
        if len(values) > 0:
            self.data_type = type(values[0])
            if not all(isinstance(v, self.data_type) for v in values):
                raise KavanaTypeError("배열의 요소는 모두 동일한 데이터 타입이어야 합니다")
        else:
            self.data_type = None
        
        self.data = list(values)
        self.value = self.data  # ✅ value를 리스트 데이터로 설정

    def to_list(self):
        """ListType을 Python의 기본 list로 변환하여 반환"""
        return self.data[:]  # ✅ 리스트의 복사본을 반환
    
    def append(self, value):
        """요소를 리스트 끝에 추가"""
        if self.data_type is None:
            self.data_type = type(value)
        elif not isinstance(value, self.data_type):
            raise KavanaTypeError("배열의 요소는 모두 동일한 데이터 타입이어야 합니다")
        
        self.data.append(value)

    def insert(self, index, value):
        """지정된 위치에 요소 삽입"""
        if self.data_type is None:
            self.data_type = type(value)
        elif not isinstance(value, self.data_type):
            raise KavanaTypeError("배열의 요소는 모두 동일한 데이터 타입이어야 합니다")
        
        if 0 <= index <= len(self.data):
            self.data.insert(index, value)
        else:
            raise KavanaIndexError("배열의 인덱스가 범위를 벗어났습니다.")

    def remove(self, value):
        """요소 값을 직접 삭제 가능하도록 변경"""
        if value in self.data:
            self.data.remove(value)
        else:
            raise KavanaValueError("배열의 값을 찾을 수 없습니다.")

    def remove_at(self, index):
        """기존의 인덱스 삭제 기능 유지"""
        if 0 <= index < len(self.data):
            del self.data[index]
        else:
            raise KavanaIndexError("배열의 인덱스가 범위를 벗어났습니다.")

    def set(self, row, col=None, token=None):
        """✅ 지정된 인덱스의 값을 변경 (1차원/2차원 리스트 지원)"""
        if col is None:
            # 1차원 리스트에서 값 변경
            if 0 <= row < len(self.data):
                if self.data_type is None:
                    # 리스트가 비어 있으면 타입 결정
                    self.data_type = type(token)
                elif not isinstance(token, self.data_type):
                    raise KavanaTypeError("배열의 요소는 모두 동일한 데이터 타입이어야 합니다")
                
                self.data[row] = token
            else:
                raise KavanaIndexError("리스트의 인덱스가 범위를 벗어났습니다")
        else:
            # 2차원 리스트에서 값 변경
            if not isinstance(self.data[row], list):
                raise KavanaTypeError("배열의 요소는 모두 동일한 데이터 타입이어야 합니다")
            
            if 0 <= row < len(self.data) and 0 <= col < len(self.data[row]):
                self.data[row][col] = token
            else:
                raise IndexError("리스트의 인덱스가 범위를 벗어났습니다")


    def length(self):
        """리스트 길이 반환"""
        return len(self.data)

    def get(self, row, col=None):
        """✅ 인덱스로 요소 가져오기 (1차원/2차원 리스트 지원)"""
        if col is None:
            # 1차원 리스트에서 값 가져오기
            if 0 <= row < len(self.data):
                return self.data[row]
            else:
                raise KavanaIndexError("배열의 인덱스를 벗어났습니다(get)")
        else:
            # 2차원 리스트에서 값 가져오기
            if not isinstance(self.data[row], list):
                raise KavanaTypeError("배열의 요소가 2중배열이 아닙니다(get)")
            
            if 0 <= row < len(self.data) and 0 <= col < len(self.data[row]):
                return self.data[row][col]
            else:
                raise KavanaIndexError("배열의 인덱스를 벗어났습니다(get)")


    def __repr__(self):
        """리스트를 문자열로 변환 (내부 데이터 타입 지원)"""
        
        def extract_value(item):
            """DataType이면 value 추출, 아니면 그대로 반환"""
            if isinstance(item, Array):
                return f"[{', '.join(map(str, (extract_value(i) for i in item.data.primitive)))}]"  # ListType 내부 변환
            return item.value if hasattr(item, 'value') else item  # Integer, Float 등 지원

        values_str = ", ".join(map(str, (extract_value(item) for item in self.data)))
        return f"[{values_str}]"

    @property    
    def string(self):
        """✅ 항상 문자열(str)로 변환, ListType이면 '[ ]'를 붙여 출력"""
        from lib.core.token import Token, ArrayToken  # 필요한 토큰 불러오기

        def extract_value(item):
            """DataType이면 value 추출, ListType이면 재귀적으로 변환"""
            
            # ✅ 리스트 타입이면 내부 요소를 변환
            if isinstance(item, Array):
                converted_elements = [extract_value(i) for i in item.data]
                return f"[{', '.join(map(str, converted_elements))}]"

            # ✅ ListExToken인 경우, 내부의 `element_expresses`에서 값을 추출
            if isinstance(item, ArrayToken):
                flattened_values = []
                for element_group in item.element_expresses:  # [[Token], [Token], [Token]]
                    for token in element_group:
                        flattened_values.append(extract_value(token))  # Token을 변환
                return f"[{', '.join(map(str, flattened_values))}]"
            
            if isinstance(item, list):
                converted_elements = [extract_value(i) for i in item]
                return f"[{', '.join(map(str, converted_elements))}]"

            # ✅ Token이면 data.value를 사용하여 primitive 값 추출
            if isinstance(item, Token) and hasattr(item, "data"):
                return item.data.string if hasattr(item.data, "value") else str(item.data.value)

            # ✅ 일반적인 데이터 타입 (Integer, Float 등)
            return item.value if hasattr(item, "value") else str(item)

        # ✅ self.data 내부 요소를 변환
        converted_list = [extract_value(item) for item in self.data]
        return f"[{', '.join(map(str, converted_list))}]"


    @property
    def primitive(self):
        """Python list로 변환"""
        return self.data.copy()  # ✅ Python 리스트 반환
