from lib.core.datatypes.kavana_datatype import KavanaDataType

class ListType(KavanaDataType):
    def __init__(self, *values):
        if len(values) > 0:
            self.data_type = type(values[0])
            if not all(isinstance(v, self.data_type) for v in values):
                raise TypeError("All elements in the list must be of the same type")
        else:
            self.data_type = None
        
        self.data = list(values)
        self.value = self.data  # ✅ value를 리스트 데이터로 설정

    def append(self, value):
        """요소를 리스트 끝에 추가"""
        if self.data_type is None:
            self.data_type = type(value)
        elif not isinstance(value, self.data_type):
            raise TypeError("All elements in the list must be of the same type")
        
        self.data.append(value)

    def insert(self, index, value):
        """지정된 위치에 요소 삽입"""
        if self.data_type is None:
            self.data_type = type(value)
        elif not isinstance(value, self.data_type):
            raise TypeError("All elements in the list must be of the same type")
        
        if 0 <= index <= len(self.data):
            self.data.insert(index, value)
        else:
            raise IndexError("List index out of range")

    def remove(self, value):
        """요소 값을 직접 삭제 가능하도록 변경"""
        if value in self.data:
            self.data.remove(value)
        else:
            raise ValueError("Value not found in list")

    def remove_at(self, index):
        """기존의 인덱스 삭제 기능 유지"""
        if 0 <= index < len(self.data):
            del self.data[index]
        else:
            raise IndexError("List index out of range")

    def set(self, row, col=None, value=None):
        """✅ 지정된 인덱스의 값을 변경 (1차원/2차원 리스트 지원)"""
        if col is None:
            # 1차원 리스트에서 값 변경
            if 0 <= row < len(self.data):
                if self.data_type is None:
                    # 리스트가 비어 있으면 타입 결정
                    self.data_type = type(value)
                elif not isinstance(value, self.data_type):
                    raise TypeError("All elements in the list must be of the same type")
                
                self.data[row] = value
            else:
                raise IndexError("List index out of range")
        else:
            # 2차원 리스트에서 값 변경
            if not isinstance(self.data[row], list):
                raise TypeError("Attempting to set a value in a non-list element")
            
            if 0 <= row < len(self.data) and 0 <= col < len(self.data[row]):
                self.data[row][col] = value
            else:
                raise IndexError("List index out of range")


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
                raise IndexError("리스트의 인덱스를 벗어났습니다")
        else:
            # 2차원 리스트에서 값 가져오기
            if not isinstance(self.data[row], list):
                raise TypeError("배열의 요소가 2중배열이 아닙니다")
            
            if 0 <= row < len(self.data) and 0 <= col < len(self.data[row]):
                return self.data[row][col]
            else:
                raise IndexError("리스트의 인덱스를 벗어났습니다")


    def __repr__(self):
        """리스트를 문자열로 변환 (내부 데이터 타입 지원)"""
        
        def extract_value(item):
            """DataType이면 value 추출, 아니면 그대로 반환"""
            if isinstance(item, ListType):
                return f"[{', '.join(map(str, (extract_value(i) for i in item.data.primitive)))}]"  # ListType 내부 변환
            return item.value if hasattr(item, 'value') else item  # Integer, Float 등 지원

        values_str = ", ".join(map(str, (extract_value(item) for item in self.data)))
        return f"{values_str}"


    @property
    def string(self):
        """✅ 항상 문자열(str)로 변환, ListType이면 '[ ]'를 붙여 출력"""
        
        def extract_value(item):
            """DataType이면 value 추출, ListType이면 재귀적으로 변환"""
            if isinstance(item, ListType):
                return f"[{', '.join(map(str, (extract_value(i) for i in item.data)))}]"  # ListType 내부 처리
            return item.value if hasattr(item, 'value') else item  # Integer, Float 등 지원

        values_str = ", ".join(map(str, (extract_value(item) for item in self.data)))
        return f"[{values_str}]"


    @property
    def primitive(self):
        """Python list로 변환"""
        return self.data.copy()  # ✅ Python 리스트 반환
