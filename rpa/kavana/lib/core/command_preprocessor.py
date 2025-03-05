import re
from typing import List

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
    
    def __init__(self, script_lines=[]):
        self.script_lines = script_lines  # 빈 줄 포함하여 유지

    def get_leading_space_info(self, line):
        """
        탭을 변환하면서 실제 앞쪽 공백 개수 및 시작 컬럼 위치 반환
        - 탭(`\t`)은 공백 4개로 변환
        """
        column_position = 1  # 실제 시작 컬럼 위치
        
        for char in line:
            if char == "\t":
                tab_size = 4 - ((column_position - 1) % 4)  # 현재 위치에서 4의 배수가 되도록 설정
                column_position += tab_size
            elif char == " ":
                column_position += 1
            else:
                break  # 처음 공백이 끝나면 종료

        return  column_position  # **정확한 시작 컬럼 번호를 반환**

    def preprocess(self, script_lines=[],remove_comments=True) -> List[ PreprocessedLine ]:
        """스크립트를 전처리하여 줄 병합 및 주석 제거를 수행"""
        if script_lines:
            self.script_lines = script_lines
        merged_lines = []
        current_line = ""
        merging = False  # 여러 줄 병합 중인지 여부
        merged_column_start = 0  # 병합 시작 컬럼
        last_line_num = None  # 마지막 줄 번호 추적

        for i, line in enumerate(self.script_lines):
            original_line_num = i + 1  # 줄 번호를 1부터 유지 (빈 줄 포함)

            original_column_start = self.get_leading_space_info(line)  # 정확한 컬럼 정보 가져오기

            # 주석 제거
            if remove_comments:
                line = re.sub(r'//.*', '', line).rstrip()

            # 빈 줄은 추가하지 않음
            if not line.strip():
                continue

            # 줄 병합 처리 (`\`로 끝나는 줄을 병합)
            if line.rstrip().endswith("\\"):
                if not merging:
                    merging = True
                    merged_column_start = original_column_start  # 병합 시작 위치 저장
                    last_line_num = original_line_num  # 병합 시작 줄 번호 저장
                current_line = current_line.rstrip() + line[:-1]  # ✅ 백슬래시 제거 후 공백 유지
            else:
                # ✅ `merging = True`일 때만 공백 유지
                if merging:
                    current_line += line  # ✅ 앞 공백 유지하면서 병합
                else:
                    current_line += line.strip()  # 일반 줄에서는 불필요한 공백 제거

                final_column_start = merged_column_start if merging else original_column_start

                # 병합된 경우, 기존 줄 번호를 유지하고 추가
                merged_lines.append(PreprocessedLine(current_line, last_line_num if merging else original_line_num, final_column_start))

                # 초기화
                current_line = ""
                merging = False
                last_line_num = None  # 병합 끝났으므로 초기화

        return merged_lines
