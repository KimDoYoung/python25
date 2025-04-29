from lib.core.builtins.rpa_functions import RpaFunctions
from lib.core.token_custom import WindowToken
from lib.core.token_type import TokenType


t = RpaFunctions.WINDOW_LIST()
assert t.type == TokenType.ARRAY, "Expected type ARRAY"
assert len(t.data.value) > 0, "Expected non-empty array"
for item in t.data.value:
    assert isinstance(item, WindowToken), "Expected type WindowToken"
    assert item.data.hwnd is not None, "Expected hwnd to be not None"
    assert item.data.title is not None, "Expected title to be not None"
    assert item.data.class_name is not None, "Expected class_name to be not None"
    print(f"Window: {item.data.title}, Hwnd: {item.data.hwnd}, Class Name: {item.data.class_name}")

print("----------------------------------------------------------------")
# efplusmain.exe
process_name = "efplusmain.exe"
t = RpaFunctions.WINDOW_LIST(process_name=process_name)
assert t.type == TokenType.ARRAY, "Expected type ARRAY"
assert len(t.data.value) > 0, "Expected non-empty array"
for item in t.data.value:
    assert isinstance(item, WindowToken), "Expected type WindowToken"
    assert item.data.hwnd is not None, "Expected hwnd to be not None"
    assert item.data.title is not None, "Expected title to be not None"
    assert item.data.class_name is not None, "Expected class_name to be not None"
    print(f"title: {item.data.title}, Hwnd: {item.data.hwnd}, Class Name: {item.data.class_name}")

for item in t.data.value:
    if item.data.title == "eFriend Plus(64bit)":
        hwnd = item.data.hwnd
        break

top_window = RpaFunctions.WINDOW_TOP(process_name=process_name)
print(f"Top Window: {top_window.data.title}, Hwnd: {top_window.data.hwnd}, Class Name: {top_window.data.class_name}")

region_token = RpaFunctions.WINDOW_REGION(hwnd=top_window.data.hwnd)
print(f"Region: {region_token.data}")  # Expecting a tuple (x, y, width, height)    