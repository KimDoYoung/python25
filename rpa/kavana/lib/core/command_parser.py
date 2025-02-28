import re

class PreprocessedLine:
    """원본 코드의 줄 정보와 컬럼을 유지한 상태로 변환된 줄을 저장"""
    def __init__(self, text, original_line, original_column):
        self.text = text.strip()  # 변환된 텍스트
        self.original_line = original_line  # 원본 줄 번호
        self.original_column = original_column  # 원본 컬럼 시작 위치

    def __repr__(self):
        return f"PreprocessedLine(line={self.original_line}, col={self.original_column}, text={self.text})"


class CommandPreprocessor:
    """스크립트 전처리기: 주석 제거, 줄 병합 등을 수행하면서 원본 줄 번호와 컬럼을 유지"""
    
    def __init__(self, script_lines):
        self.script_lines = script_lines

    def get_leading_space_count(self, line):
        """탭을 변환하면서 실제 앞쪽 공백 개수를 반환 (탭 1개 = 4칸)"""
        space_count = 0
        for char in line:
            if char == "\t":
                space_count += 4 - (space_count % 4)  # 현재 위치에서 4의 배수가 되도록 설정
            elif char == " ":
                space_count += 1
            else:
                break
        return space_count

    def preprocess(self, remove_comments=True):
        """스크립트를 전처리하여 줄 병합 및 주석 제거를 수행"""
        merged_lines = []
        current_line = ""
        merging = False  # 여러 줄 병합 중인지 여부
        merged_column_start = 0  # 병합 시작 컬럼 (초기값)

        for i, line in enumerate(self.script_lines):
            if not line.strip():
                continue  # 빈 줄 스킵

            original_line_num = i + 1
            original_column_start = self.get_leading_space_count(line)  # 올바른 컬럼 정보 계산

            # 주석 제거
            if remove_comments:
                line = re.sub(r'//.*', '', line).rstrip()

            # 줄 병합 처리
            if line.rstrip().endswith("\\"):  
                if not merging:
                    merging = True
                    merged_column_start = original_column_start  # 병합 시작 위치 저장
                current_line += line.rstrip()[:-1]  # 백슬래시 제거 후 병합
            else:
                current_line += " " + line.lstrip()
                final_column_start = merged_column_start if merging else original_column_start
                merged_lines.append(PreprocessedLine(current_line.strip(), original_line_num, final_column_start))
                
                # 초기화
                current_line = ""
                merging = False

        return merged_lines
