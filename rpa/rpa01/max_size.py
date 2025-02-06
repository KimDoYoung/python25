import time
from pywinauto import Application

full_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# 크롬 브라우저 실행
app = Application(backend="win32").start(full_path)

# 창이 열릴 때까지 잠시 대기
time.sleep(2)

# 창 핸들링 (크롬 창 제목은 동적으로 변경될 수 있음)
window = app.window(title_re=".*Chrome.*")

# 창 최대화
window.maximize()

# 창이 최대화되었는지 확인
if window.is_maximized():
    print("크롬 창이 최대화되었습니다.")
else:
    print("크롬 창을 최대화하지 못했습니다.")