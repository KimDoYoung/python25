from lib.core.function_parser import FunctionParser
from lib.core.function_registry import FunctionRegistry


def register_my_func():
    FunctionRegistry.register_function('my_func', ['a', 'b'], 'print a')

register_my_func()
tokens = ["my_func", "(", "3", "4", ")"]
func_name = tokens[0].upper()
func_info = FunctionRegistry.get_function(func_name)
arg_count = func_info["arg_count"]
result, _ = FunctionParser._parse_function_call(tokens, 0, None,  arg_count)    
print(result)  # Expected my_func(3,4)

tokens = ["my_func", "(", "(", "3", ")", "(", "4", ")", ")"] # ["MY_FUNC((3),(4))"]
func_name = tokens[0].upper()
func_info = FunctionRegistry.get_function(func_name)
arg_count = func_info["arg_count"]
result, _ = FunctionParser._parse_function_call(tokens, 0,  None, arg_count)    
print(result)  # Expected my_func((3),(4))

tokens=["my_func", "(", "length", "(", '"abc"', ")", "4", ")"] # ["MY_FUNC(length(\"abc\"),4)"]
func_name = tokens[0].upper()
func_info = FunctionRegistry.get_function(func_name)
arg_count = func_info["arg_count"]
result, _ = FunctionParser._parse_function_call(tokens, 0,  None, arg_count)    
print(result)  # Expected my_func(3,4)

tokens = ["my_func", "(", ")"] #, ["MY_FUNC()"]),
func_name = tokens[0].upper()
func_info = FunctionRegistry.get_function(func_name)
arg_count = func_info["arg_count"]
result, _ = FunctionParser._parse_function_call(tokens, 0,  None, arg_count) 
print(result)  # Expected my_func()

tokens = ["my_func", "(", "length", "(", '"abc"', ")", "substr", "(", '"123"', "1", "2", ")", ")"]
func_name = tokens[0].upper()
func_info = FunctionRegistry.get_function(func_name)
arg_count = func_info["arg_count"]
result, _ = FunctionParser._parse_function_call(tokens, 0,  None, arg_count) 
print(result)  # Expected my_func()

