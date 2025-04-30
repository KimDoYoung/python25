import pytest
from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

@pytest.fixture
def script():
    return """
    main
        SET p = Point(10,20)
        SET rt = Rectangle(0,0,10,20)
        SET rg = Region(1,1,100,200)
        SET win1 = WINDOW("title1", 0, "aaa")
        SET img1 = Image("C:/tmp/1.png")
        SET app1 = Application("notepad.exe","abc")
        print f"{p}, {rt}, {rg}, {win1}, {img1}"
    end_main
    """

def test_script_execution(script, capsys):
    """✅ Kavana 스크립트 실행 테스트"""
    
    # ✅ 스크립트 전처리
    script_lines = script.split("\n")
    command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)

    # ✅ 파싱
    parser = CommandParser()
    parsed_commands = parser.parse(command_preprocssed_lines)

    # ✅ 실행
    commandExecutor = CommandExecutor()
    for command in parsed_commands:
        commandExecutor.execute(command)

    # ✅ `print` 결과 확인
    captured = capsys.readouterr()
    expected_output = "(10, 20), [0, 0, 10, 20], [1, 1, 100, 200], title1, C:/tmp/1.png\n"
    
    assert expected_output in captured.out, f"출력값이 예상과 다릅니다: {captured.out}"
