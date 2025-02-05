import pyautogui
import time

# 1. 윈도우 + R을 눌러 실행 창 열기
pyautogui.hotkey('win', 'r')
time.sleep(1)

# 2. 'notepad' 입력 후 Enter
pyautogui.write('notepad')
pyautogui.press('enter')
time.sleep(1)

# 3. 메모장에 텍스트 입력
pyautogui.write('안녕하세요! PyAutoGUI로 자동화 중입니다.', interval=0.1)

# 4. 파일 저장 (Ctrl + S)
pyautogui.hotkey('ctrl', 's')
time.sleep(1)

# 5. 파일명 입력 후 저장
pyautogui.write('자동화_테스트.txt')
pyautogui.press('enter')
