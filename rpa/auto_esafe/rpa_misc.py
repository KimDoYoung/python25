
import time
import pyautogui
import pyperclip


def is_similar_color(color1, color2, tolerance=10):
    """
    두 개의 RGB 색상이 비슷한지 확인 (tolerance 값 내에서 허용)
    :param color1: 기준 색상 (예: (34, 177, 76))
    :param color2: 비교할 색상 (예: (36, 180, 78))
    :param tolerance: 허용할 오차 범위 (기본값 10)
    :return: 비슷하면 True, 아니면 False
    """
    return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1, color2))

def get_text_from_input_field():
    """
    현재 포커스된 입력창의 텍스트를 클립보드에서 가져오는 함수.
    
    1. 현재 포커스를 맞춘 상태에서 Ctrl + A (전체 선택)
    2. Ctrl + C (클립보드 복사)
    3. 클립보드에서 텍스트 읽어오기
    """
    pyautogui.hotkey('ctrl', 'a')  # 전체 선택
    time.sleep(0.2)  # 안정적인 동작을 위해 잠깐 대기
    pyautogui.hotkey('ctrl', 'c')  # 복사
    time.sleep(0.2)  # 복사될 시간을 확보
    return pyperclip.paste().strip()  # 클립보드에서 텍스트 가져오기