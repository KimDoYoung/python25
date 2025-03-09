from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil

# 대입
script = """
MAIN
    //SET olist = [1, 2, 3, 4, 5]
    //set a[1] = 3
    //set a = [1,olist[3],4] 
    //set a = [1,a[1],4]
    //a = [1,2,3] //-> a,=,ListExToken
    //a = list[1] //-> a,=,ListIndexToken 
    // set a=b[c[2,3]+1]  + 9 
    // set a = [ [1,2], [3,4] ]
    // set a = [1,2,3] 
    set a = [ [1,2], [3,4] ]
END_MAIN
"""
#---------------------------
# 기본적인 사용
#---------------------------

script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
for line in command_preprocssed_lines:
    # print(line)
    if 'MAIN' in line.text:
        continue
    tokens = CommandParser().tokenize(line)
    # print(TokenUtil.tokens_to_string(tokens))
    # r,c,i = CommandParser().extract_row_column_expresses(tokens,4)
    # print(i)
    # print(TokenUtil.tokens_to_string(r))
    # print(TokenUtil.tokens_to_string(c))

    # r,c,i = CommandParser().extract_row_column_expresses(tokens,6)
    # print(i)
    # print(TokenUtil.tokens_to_string(r))
    # print(TokenUtil.tokens_to_string(c))

    # post_tokens= CommandParser().post_process_tokens(tokens)
    print("----------------------------")
    for token in tokens:
        if token.type == TokenType.LIST_EX:
            elements = []
            for express in token.element_expresses:
                elements.append(TokenUtil.tokens_to_string(express))
            elements_str = ', '.join(elements)    
            print(token.type, f"length:{len(token.element_expresses)}, els:{elements_str}")
        elif token.type == TokenType.LIST_INDEX:
            row_express_str = TokenUtil.tokens_to_string(token.row_express)
            column_express_str = TokenUtil.tokens_to_string(token.column_express)
            print(token.type, f"name:{token.data.value}, row,col:{row_express_str},{column_express_str}")
        else:
            print(token.type,token.data.value)
    print("----------------------------")
