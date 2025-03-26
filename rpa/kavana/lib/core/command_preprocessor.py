import re
from typing import List

from lib.core.exceptions.kavana_exception import KavanaSyntaxError

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

    
    # def preprocess(self, script_lines=[], remove_comments=True) -> List[PreprocessedLine]:
    #     if script_lines:
    #         self.script_lines = script_lines
    #     merged_lines = []
    #     current_line = ""
    #     merging = False
    #     merged_column_start = 0
    #     last_line_num = None
    #     open_brace_count = 0
    #     open_bracket_count = 0
    #     inside_string = False
    #     # """...""" 문자열 처리용 변수들
    #     inside_multiline_string = False
    #     multiline_string_delimiter = '"""'        

    #     for i, line in enumerate(self.script_lines):
    #         if not line.strip():
    #             continue

    #         original_line_num = i + 1
    #         original_column_start = self.get_leading_space_info(line)

    #         if remove_comments:
    #             line = re.sub(r'//.*', '', line).rstrip()

    #         line_stripped = line.strip()

    #         # ✅ 멀티라인 문자열 시작/종료 감지
    #         if multiline_string_delimiter in line:
    #             count = line.count(multiline_string_delimiter)
    #             if count % 2 == 1:
    #                 inside_multiline_string = not inside_multiline_string

    #         if merging:
    #             current_line += " " + line_stripped
    #         else:
    #             current_line = line_stripped
    #             merged_column_start = original_column_start
    #             last_line_num = original_line_num

    #         if not inside_multiline_string:
    #             for char in line:
    #                 if char == '"':
    #                     inside_string = not inside_string
    #                 elif not inside_string:
    #                     if char == "[":
    #                         open_bracket_count += 1
    #                     elif char == "]":
    #                         open_bracket_count -= 1
    #                     elif char == "{":
    #                         open_brace_count += 1
    #                     elif char == "}":
    #                         open_brace_count -= 1

    #             # 불일치한 괄호 감지
    #             if open_bracket_count < 0:
    #                 raise KavanaSyntaxError(f"대괄호 ']'가 너무 많이 닫혔습니다: {original_line_num}번째 줄")
    #             if open_brace_count < 0:
    #                 raise KavanaSyntaxError(f"중괄호 '}}'가 너무 많이 닫혔습니다: {original_line_num}번째 줄")

    #         merging = (open_brace_count > 0 or open_bracket_count > 0 or inside_multiline_string)

    #         if not merging and (open_brace_count == 0 and open_bracket_count == 0 and not inside_multiline_string):
    #             if inside_string:
    #                 raise KavanaSyntaxError(f"문자열 리터럴이 닫히지 않았습니다: {original_line_num}번째 줄")
    #             merged_lines.append(PreprocessedLine(current_line.strip(), last_line_num, merged_column_start))
    #             current_line = ""
    #             last_line_num = None

    #     # 파일이 끝났는데 괄호가 안 닫힘
    #     if open_bracket_count > 0:
    #         raise KavanaSyntaxError("리스트 인덱싱의 괄호가 올바르게 닫히지 않았습니다.")
    #     if open_brace_count > 0:
    #         raise KavanaSyntaxError("맵 정의의 중괄호가 올바르게 닫히지 않았습니다.")
    #     if inside_string:
    #         raise KavanaSyntaxError("문자열 리터럴이 닫히지 않았습니다.")

    #     return merged_lines

    # def preprocess(self, script_lines=[], remove_comments=True) -> List[PreprocessedLine]:
    #     if script_lines:
    #         self.script_lines = script_lines
    #     merged_lines = []
    #     current_line = ""
    #     merging = False
    #     merged_column_start = 0
    #     last_line_num = None
    #     open_brace_count = 0
    #     open_bracket_count = 0
    #     inside_string = False
    #     inside_multiline_string = False
    #     multiline_string_delimiter = '"""'

    #     for i, line in enumerate(self.script_lines):
    #         if not line.strip():
    #             continue

    #         original_line_num = i + 1
    #         original_column_start = self.get_leading_space_info(line)

    #         if remove_comments and not inside_multiline_string:
    #             line = re.sub(r'//.*', '', line).rstrip()

    #         line_stripped = line.strip()

    #         # ✅ 이 줄에서 멀티라인 문자열 토글이 일어날지 미리 확인
    #         toggle_multiline_string = False
    #         if multiline_string_delimiter in line:
    #             count = line.count(multiline_string_delimiter)
    #             if count % 2 == 1:
    #                 toggle_multiline_string = True

    #         if merging:
    #             current_line += " " + line_stripped
    #         else:
    #             current_line = line_stripped
    #             merged_column_start = original_column_start
    #             last_line_num = original_line_num

    #         # ✅ 괄호 및 문자열 처리 (멀티라인 문자열 안에서는 생략)
    #         if not inside_multiline_string:
    #             for char in line:
    #                 if char == '"':
    #                     inside_string = not inside_string
    #                 elif not inside_string:
    #                     if char == "[":
    #                         open_bracket_count += 1
    #                     elif char == "]":
    #                         open_bracket_count -= 1
    #                     elif char == "{":
    #                         open_brace_count += 1
    #                     elif char == "}":
    #                         open_brace_count -= 1

    #             # 불일치한 괄호 감지
    #             if open_bracket_count < 0:
    #                 raise KavanaSyntaxError(f"대괄호 ']'가 너무 많이 닫혔습니다: {original_line_num}번째 줄")
    #             if open_brace_count < 0:
    #                 raise KavanaSyntaxError(f"중괄호 '}}'가 너무 많이 닫혔습니다: {original_line_num}번째 줄")

    #         # ✅ 병합 여부 판단
    #         merging = (open_brace_count > 0 or open_bracket_count > 0 or inside_multiline_string)

    #         # ✅ 병합 종료 시점
    #         if not merging and (open_brace_count == 0 and open_bracket_count == 0 and not inside_multiline_string):
    #             if inside_string:
    #                 raise KavanaSyntaxError(f"문자열 리터럴이 닫히지 않았습니다: {original_line_num}번째 줄")
    #             merged_lines.append(PreprocessedLine(current_line.strip(), last_line_num, merged_column_start))
    #             current_line = ""
    #             last_line_num = None

    #         # ✅ 멀티라인 문자열 상태 토글은 줄 끝에서 수행
    #         if toggle_multiline_string:
    #             inside_multiline_string = not inside_multiline_string

    #     # ✅ 최종 종료 검사
    #     if open_bracket_count > 0:
    #         raise KavanaSyntaxError("리스트 인덱싱의 괄호가 올바르게 닫히지 않았습니다.")
    #     if open_brace_count > 0:
    #         raise KavanaSyntaxError("맵 정의의 중괄호가 올바르게 닫히지 않았습니다.")
    #     if inside_string:
    #         raise KavanaSyntaxError("문자열 리터럴이 닫히지 않았습니다.")
    #     if inside_multiline_string:
    #         raise KavanaSyntaxError('멀티라인 문자열("""...""")이 닫히지 않았습니다.')

    #     return merged_lines

    # def preprocess(self, script_lines=[], remove_comments=True) -> List[PreprocessedLine]:
    #     if script_lines:
    #         self.script_lines = script_lines
    #     merged_lines = []
    #     current_line = ""
    #     merging = False
    #     merged_column_start = 0
    #     last_line_num = None
    #     open_brace_count = 0
    #     open_bracket_count = 0
    #     inside_string = False
    #     inside_multiline_string = False
    #     multiline_string_delimiter = '"""'

    #     for i, line in enumerate(self.script_lines):
    #         if not line.strip():
    #             continue

    #         original_line_num = i + 1
    #         original_column_start = self.get_leading_space_info(line)

    #         # ✅ 상태 백업
    #         was_inside_multiline_string = inside_multiline_string
    #         toggle_multiline_string = False

    #         # ✅ 멀티라인 문자열 시작/종료 감지 (상태는 줄 처리 후에 토글)
    #         if multiline_string_delimiter in line:
    #             count = line.count(multiline_string_delimiter)
    #             if count % 2 == 1:
    #                 toggle_multiline_string = True

    #         # ✅ 주석 제거 (멀티라인 문자열 안이 아닐 때만)
    #         if remove_comments and not was_inside_multiline_string:
    #             line = re.sub(r'//.*', '', line).rstrip()

    #         line_stripped = line.strip()

    #         # ✅ 줄 병합 처리
    #         if merging:
    #             current_line += " " + line_stripped
    #         else:
    #             current_line = line_stripped
    #             merged_column_start = original_column_start
    #             last_line_num = original_line_num

    #         # ✅ 괄호 및 문자열 처리 (멀티라인 문자열 내부일 때는 건너뜀)
    #         if not was_inside_multiline_string:
    #             for char in line:
    #                 if char == '"':
    #                     inside_string = not inside_string
    #                 elif not inside_string:
    #                     if char == "[":
    #                         open_bracket_count += 1
    #                     elif char == "]":
    #                         open_bracket_count -= 1
    #                     elif char == "{":
    #                         open_brace_count += 1
    #                     elif char == "}":
    #                         open_brace_count -= 1

    #             # 불일치한 괄호 감지
    #             if open_bracket_count < 0:
    #                 raise KavanaSyntaxError(f"대괄호 ']'가 너무 많이 닫혔습니다: {original_line_num}번째 줄")
    #             if open_brace_count < 0:
    #                 raise KavanaSyntaxError(f"중괄호 '}}'가 너무 많이 닫혔습니다: {original_line_num}번째 줄")

    #         # ✅ 병합 여부 결정
    #         merging = (open_brace_count > 0 or open_bracket_count > 0 or inside_multiline_string)

    #         # ✅ 병합 종료 시점
    #         if not merging and (open_brace_count == 0 and open_bracket_count == 0 and not inside_multiline_string):
    #             if inside_string:
    #                 raise KavanaSyntaxError(f"문자열 리터럴이 닫히지 않았습니다: {original_line_num}번째 줄")
    #             merged_lines.append(PreprocessedLine(current_line.strip(), last_line_num, merged_column_start))
    #             current_line = ""
    #             last_line_num = None

    #         # ✅ 줄 끝난 후 멀티라인 문자열 상태 토글
    #         if toggle_multiline_string:
    #             inside_multiline_string = not inside_multiline_string

    #     # ✅ 종료 검사
    #     if open_bracket_count > 0:
    #         raise KavanaSyntaxError("리스트 인덱싱의 괄호가 올바르게 닫히지 않았습니다.")
    #     if open_brace_count > 0:
    #         raise KavanaSyntaxError("맵 정의의 중괄호가 올바르게 닫히지 않았습니다.")
    #     if inside_string:
    #         raise KavanaSyntaxError("문자열 리터럴이 닫히지 않았습니다.")
    #     if inside_multiline_string:
    #         raise KavanaSyntaxError('멀티라인 문자열("""...""")이 닫히지 않았습니다.')

    #     return merged_lines

    def preprocess(self, script_lines=[], remove_comments=True) -> List[PreprocessedLine]:
        if script_lines:
            self.script_lines = script_lines

        merged_lines = []
        current_line = ""
        last_line_num = None
        merged_column_start = 0

        open_bracket_count = 0
        open_brace_count = 0
        inside_string = False

        def update_structure_depth(line: str):
            nonlocal open_bracket_count, open_brace_count, inside_string
            for char in line:
                if char == '"':
                    inside_string = not inside_string
                elif not inside_string:
                    if char == "[":
                        open_bracket_count += 1
                    elif char == "]":
                        open_bracket_count -= 1
                    elif char == "{":
                        open_brace_count += 1
                    elif char == "}":
                        open_brace_count -= 1

        def is_structure_open() -> bool:
            return open_bracket_count > 0 or open_brace_count > 0

        for i, line in enumerate(self.script_lines):
            if not line.strip():
                continue

            original_line_num = i + 1
            original_column_start = self.get_leading_space_info(line)

            if remove_comments:
                line = re.sub(r'//.*', '', line).rstrip()

            line_stripped = line.strip()

            if current_line:
                current_line += " " + line_stripped
            else:
                current_line = line_stripped
                merged_column_start = original_column_start
                last_line_num = original_line_num

            update_structure_depth(line)

            if open_bracket_count < 0:
                raise KavanaSyntaxError(f"대괄호 ']'가 너무 많이 닫혔습니다: {original_line_num}번째 줄")
            if open_brace_count < 0:
                raise KavanaSyntaxError(f"중괄호 '}}'가 너무 많이 닫혔습니다: {original_line_num}번째 줄")

            if not is_structure_open():
                if inside_string:
                    raise KavanaSyntaxError(f"문자열 리터럴이 닫히지 않았습니다: {original_line_num}번째 줄")
                merged_lines.append(PreprocessedLine(current_line.strip(), last_line_num, merged_column_start))
                current_line = ""
                last_line_num = None

        if is_structure_open():
            raise KavanaSyntaxError("괄호가 올바르게 닫히지 않았습니다.")
        if inside_string:
            raise KavanaSyntaxError("문자열 리터럴이 닫히지 않았습니다.")

        return merged_lines
