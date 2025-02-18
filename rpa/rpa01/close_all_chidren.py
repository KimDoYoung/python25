from pywinauto import Application

# HTS 프로그램 실행 또는 연결
title = "eFriend Plus"
app = Application().connect(title=title)  # HTS 창 연결
main_window = app.window(title=title)  # 메인 윈도우 접근

# MDIClient 컨트롤 찾기
mdi_client = main_window.child_window(class_name="MDIClient")

# 모든 자식 창 닫기
for child in mdi_client.children():
    print(f"Closing: {child.window_text()}")  # 창 이름 출력
    child.close()
