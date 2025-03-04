from lib.core.datatypes.kavana_datatype import KavanaDataType

class ListType(KavanaDataType):
    def __init__(self, *values):
        if len(values) > 0:
            self.data_type = type(values[0])
            if not all(isinstance(v, self.data_type) for v in values):
                raise TypeError("All elements in the list must be of the same type")
            if self.data_type == ListType:
                raise TypeError("Nested lists are not allowed in ListType")
        else:
            self.data_type = None
        
        self.data = list(values)
        self.value = self.data  # ✅ value를 리스트 데이터로 설정
    
    def append(self, value):
        """요소를 리스트 끝에 추가"""
        if self.data_type is None:
            if isinstance(value, ListType):
                raise TypeError("Nested lists are not allowed in ListType")
            self.data_type = type(value)
        elif not isinstance(value, self.data_type):
            raise TypeError("All elements in the list must be of the same type")
        
        self.data.append(value)

    def insert(self, index, value):
        """지정된 위치에 요소 삽입"""
        if self.data_type is None:
            if isinstance(value, ListType):
                raise TypeError("Nested lists are not allowed in ListType")
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

    def length(self):
        """리스트 길이 반환"""
        return len(self.data)

    def get(self, index):
        """인덱스로 요소 가져오기"""
        if 0 <= index < len(self.data):
            return self.data[index]
        else:
            raise IndexError("List index out of range")

    def __repr__(self):
        """리스트를 문자열로 변환"""
        return f"LIST({', '.join(map(str, self.data))})"

    @property
    def string(self):
        """항상 문자열(str)로 변환"""
        return str(self.data)

    @property
    def primitive(self):
        """Python list로 변환"""
        return self.data.copy()  # ✅ Python 리스트 반환

# from lib.core.datatypes.kavana_datatype import KavanaDataType

# class ListType(KavanaDataType):
#     def __init__(self, *values):
#         if len(values) > 0:
#             self.data_type = type(values[0])
#             if not all(isinstance(v, self.data_type) for v in values):
#                 raise TypeError("All elements in the list must be of the same type")
#             if self.data_type == ListType:
#                 raise TypeError("Nested lists are not allowed in ListType")
#         else:
#             self.data_type = None
        
#         self.data = list(values)
#         self.value = self.data
    
#     def append(self, value):
#         if self.data_type is None:
#             if isinstance(value, ListType):
#                 raise TypeError("Nested lists are not allowed in ListType")
#             self.data_type = type(value)
#         elif not isinstance(value, self.data_type):
#             raise TypeError("All elements in the list must be of the same type")
        
#         self.data.append(value)
    
#     def insert(self, index, value):
#         """지정된 위치에 요소 삽입"""
#         if self.data_type is None:
#             if isinstance(value, ListType):
#                 raise TypeError("Nested lists are not allowed in ListType")
#             self.data_type = type(value)
#         elif not isinstance(value, self.data_type):
#             raise TypeError("All elements in the list must be of the same type")
        
#         if 0 <= index <= len(self.data):
#             self.data.insert(index, value)
#         else:
#             raise IndexError("List index out of range")
    
#     def remove(self, value):
#         """요소 값을 직접 삭제 가능하도록 변경"""
#         if value in self.data:
#             self.data.remove(value)
#         else:
#             raise ValueError("Value not found in list")
    
#     def remove_at(self, index):
#         """기존의 인덱스 삭제 기능 유지"""
#         if 0 <= index < len(self.data):
#             del self.data[index]
#         else:
#             raise IndexError("List index out of range")
    
#     def length(self):
#         return len(self.data)
    
#     def get(self, index):
#         if 0 <= index < len(self.data):
#             return self.data[index]
#         else:
#             raise IndexError("List index out of range")
    
#     def to_list(self):
#         """Python list로 변환"""
#         return self.data.copy()
    
#     def __repr__(self):
#         return f"LIST({', '.join(map(str, self.data))})"

#     @property
#     def to_string(self):
#         """항상 문자열(str)로 변환"""
#         return str(self.data)
    
#     @property
#     def to_python_type(self):
#         return self.data