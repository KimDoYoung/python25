from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    PRINT "random number: " , RANDOM(1, 10)
    PRINT "absolute value: " , ABS(5)
    PRINT "max value of 3, 7: " , MAX(3, 7)
    PRINT "min value of 3, 7: " , MIN(3, 7)
    PRINT "round 3.14: " , ROUND(3.14)
    PRINT "floor 3.14: " , FLOOR(3.14)
    PRINT "ceil 3.14: " , CEIL(3.14)
    PRINT "trunc 3.14: " , TRUNC(3.14)
    PRINT "is even 4: " , IS_EVEN(4)
    PRINT "is odd 5: " , IS_ODD(5)
    PRINT "is even 10: " , IS_EVEN(10)
    PRINT "is odd 11: " , IS_ODD(11)
    PRINT "range 1 to 10: " , RANGE(1, 10)
    PRINT "range 1 to 10 step 2: " , RANGE(1, 10, 2)
    PRINT "2^3: ", POWER(2, 3)  
    PRINT "sqrt(16): ", SQRT(16)  
    PRINT "sin(pi/2): ", SIN(3.14 / 2)
    PRINT "cos(0): ", COS(0) 
    PRINT "tan(pi/4): ", TAN(3.14 / 4) 
    PRINT "10 mod 3: ", MOD(10, 3) 
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
