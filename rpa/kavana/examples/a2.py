from lib.core.command_preprocessor import CommandPreprocessor


script = """\tMAIN
    SET a = 10
    FOR i = 1 TO \\
            a STEP 2
        PRINT "{i}"
    END_FOR
END_MAIN
"""
# script = """\tMAIN
# \tSET x = 5
# \t\t PRINT "{x}"
# END_MAIN
#     """
# script ="""MAIN
#     SET long_string = "This is a long \\
#                         string that spans \\
#                         multiple lines"
# END_MAIN
#             """
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor(script_lines).preprocess( )
for line in command_preprocssed_lines:
    print(line)
