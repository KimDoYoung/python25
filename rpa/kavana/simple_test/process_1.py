from lib.core.command_executor import CommandExecutor
from lib.core.managers.process_manager import ProcessManager


pm= ProcessManager(CommandExecutor())
wi = pm.find_top_window_info()
print(wi)

wi_list = pm.get_window_info_list("efplusmain.exe")
print("=======================")
for wi in wi_list:
    print(wi)
print("=======================")

print("MDI Top Window:", wi_list[0])
r = pm.get_window_region(wi_list[0].hwnd)
print("MDI Top Window Region:", r)

print("----------------------")
top_window = pm.find_mdi_top_window_info(3214088)
print(top_window)
print("-----------------------")
top_modal_window =  pm.find_top_modal_window("efplusmain.exe")
print("Top Modal Window:", top_modal_window)

window1 = pm.find_window_by_title("유의사항")
print("제목으로 찾은 윈도우:", window1)