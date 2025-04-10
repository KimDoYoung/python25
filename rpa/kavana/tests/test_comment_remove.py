import pytest
from lib.core.command_preprocessor import CommandPreprocessor

cp = CommandPreprocessor()

@pytest.mark.parametrize("input_line, expected_output", [
    ('BROWSER OPEN url="https://naver.com" // this is a comment',
     'BROWSER OPEN url="https://naver.com"'),

    ('SET x = 5 // 숫자 설정', 'SET x = 5'),
    
    ('PRINT "hello // world"', 'PRINT "hello // world"'),

    ('// 전체 주석인 줄', ''),
    
    ('VAR url = "https://site.com/path" // some trailing comment',
     'VAR url = "https://site.com/path"'),

    ('VAR t = "// not a comment"', 'VAR t = "// not a comment"'),

    ('VAR x = 42', 'VAR x = 42'),
])
def test_remove_comments_from_line(input_line, expected_output):
    assert cp.remove_comments_from_line(input_line) == expected_output
