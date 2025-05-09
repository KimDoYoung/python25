from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
// kavana는 primary에서만 돌아간다.
    SET monitors = MONITOR_LIST()
    for monitor in monitors
        print "111", monitor
        //if monitor["is_primary"] == True:
           //SET screen_region = Region(monitor["x"], monitor["y"], monitor["width"], monitor["height"])
           //break
        //end_if
    end_for
    //print screen_region
    set screen_region = Region(0, 0, 3000, 2000)
    set before_snap = SNAP_SCREEN_INFO(screen_region, "10x5")
    print "스크린 스냅정보저장됨"
    rpa wait seconds=10
    set changed_region = SNAP_CHANGED_REGION(before_snap, screen_region, "10x5")
    print "변경된 영역:", changed_region

END_MAIN
"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
parser = CommandParser()
parsed_commands = parser.parse(command_preprocssed_lines)

commandExecutor = CommandExecutor()

for command in parsed_commands:
    commandExecutor.execute(command)
