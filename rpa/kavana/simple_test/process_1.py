from lib.core.command_executor import CommandExecutor
from lib.core.managers.process_manager import ProcessManager


pm= ProcessManager(CommandExecutor())
wi = pm.find_top_window_info()
print(wi)

wi_list = pm.get_window_info_list("efplusmain.exe")
for wi in wi_list:
    print(wi)

print("MDI Top Window:", wi_list[0])
r = pm.get_window_region(wi_list[0].hwnd)
print("MDI Top Window Region:", r)

print("----------------------")
top_window = pm.find_mdi_top_window_info(2689692)
print(top_window)