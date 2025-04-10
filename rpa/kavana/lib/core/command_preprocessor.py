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

        # """ 멀티라인 merge용 변수
        triple_started = False  # """이 시작됨
        triple_ended = False  # """이 끝남
        triple_accumulated = "" # """으로 묶인 문자열 누적
        triple_start_info = ("", 0)  # line_num, column_start    

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

        def is_structure_opened() -> bool:
            return open_bracket_count > 0 or open_brace_count > 0
        def is_structure_closed() -> bool:
            return open_bracket_count == 0 and open_brace_count == 0

        for i, line in enumerate(self.script_lines):
            # """ 멀티라인 문자열 처리 -----------------------------------
            line_stripped = line.strip()
            triple_quote_count = line_stripped.count('"""')

            if triple_quote_count > 2:
                raise KavanaSyntaxError(f'한 줄에 """가 2번 이상 나올 수 없습니다: {i+1}번째 줄')

            if triple_quote_count == 1:
                if not triple_started:
                    triple_started = True
                    triple_accumulated = line_stripped
                    triple_start_info = (i + 1, self.get_leading_space_info(line))
                else:
                    triple_ended = True
                    triple_accumulated += '\n' + line
            elif triple_started:
                triple_accumulated += '\n' + line

            if triple_ended:
                match = re.search(r'"""(.*?)"""', triple_accumulated, flags=re.DOTALL)
                if not match:
                    raise KavanaSyntaxError(f'""" 안의 문자열을 추출할 수 없습니다: {triple_start_info[0]}번째 줄')

                inner_text = match.group(1)
                prefix = triple_accumulated.split('"""')[0].strip()
                new_line = f'{prefix}"{inner_text}"'

                merged_lines.append(PreprocessedLine(new_line, triple_start_info[0], triple_start_info[1]))

                triple_started = False
                triple_ended = False
                triple_accumulated = ""
                continue
            if triple_started:
                continue

            # 일반 로직 [, {,  등의 문자열 처리 -----------------------------------
            if not line_stripped: # 비어 있는 문자열
                continue
            original_line_num = i + 1
            original_column_start = self.get_leading_space_info(line)

            if remove_comments:
                if "//" in line:
                    line = self.remove_comments_from_line(line)
                if line.strip() == "":
                    continue

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

            if is_structure_closed():
                if inside_string:
                    raise KavanaSyntaxError(f"문자열 리터럴이 닫히지 않았습니다: {original_line_num}번째 줄")
                merged_lines.append(PreprocessedLine(current_line.strip(), last_line_num, merged_column_start))
                current_line = ""
                last_line_num = None

        if is_structure_opened():
            raise KavanaSyntaxError("괄호가 올바르게 닫히지 않았습니다.")
        if inside_string:
            raise KavanaSyntaxError("문자열 리터럴이 닫히지 않았습니다.")

        return merged_lines

    def remove_comments_from_line(self, line: str) -> str:
        in_string = False
        quote_char = ''
        result = ''
        i = 0
        while i < len(line):
            char = line[i]

            if char in ('"', "'"):
                if not in_string:
                    in_string = True
                    quote_char = char
                elif char == quote_char:
                    in_string = False
                result += char
                i += 1
                continue

            if char == '/' and i + 1 < len(line) and line[i + 1] == '/' and not in_string:
                break  # 주석 시작 → 이후 다 제거
            else:
                result += char
            i += 1

        return result.strip()
