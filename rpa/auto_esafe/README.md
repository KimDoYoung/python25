# auto_esafe

## 개요

1. eSAFE2019을 실행
2. 공인인증서로 로그인(하드에 존재)
3. 화면번호를 입력
4. 파일 다운로드
5. 종료

## 제약조건

1. 화면 크기 FHD에서 동작
2. 공인인증서는 하드에 존재.

## 기능

1. .env를 사용함. password저장
2. config에 상수 보관
3. log폴더에 auto_esafe_yyyy_mm_dd.log 생성
4. 매일 특정시간에 동작하는 것을 기본으로 함(window자체 scheduler사용)

## 참조 소스

```python
import subprocess
import time
import logging
import pyautogui
import sys

from config import Config
from utils import wait_for_image, get_region, RegionName

# 로깅 설정
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class AutomationProcess:
    def __init__(self):
        # 작업할 화면 영역 (예: 중앙 영역)
        self.region = get_region(RegionName.CENTER)
        self.process = None

    def launch_program(self):
        """
        프로그램을 실행시키고 초기 대기 시간을 둡니다.
        """
        try:
            program_path = Config.PROGRAM_PATH
            log.info(f"프로그램 실행: {program_path}")
            self.process = subprocess.Popen(program_path)
            time.sleep(5)  # 프로그램이 완전히 실행될 때까지 대기
            log.info("프로그램 실행 완료")
        except Exception as e:
            raise Exception(f"프로그램 실행 중 오류 발생: {e}")

    def click_ui_element(self, image_path, grayscale=False, sleep_after=0, error_message="요소를 찾을 수 없습니다."):
        """
        지정한 이미지 요소를 화면에서 찾은 후 클릭합니다.
        이미지 요소를 찾지 못하면 예외를 발생시킵니다.
        """
        log.info(f"이미지 탐색 시작: {image_path}")
        element = wait_for_image(image_path, region=self.region, grayscale=grayscale)
        if not element:
            raise Exception(error_message)
        pyautogui.click(pyautogui.center(element))
        log.info(f"이미지 클릭 완료: {image_path}")
        if sleep_after:
            time.sleep(sleep_after)

    def perform_login(self):
        """
        로그인 관련 UI 동작을 수행합니다.
        각 단계에서 에러 발생 시 예외를 전달합니다.
        """
        # 1. 로그인 버튼 클릭
        self.click_ui_element(
            image_path='./images/login_button.png',
            sleep_after=2,
            error_message="로그인 화면이 나타나지 않았습니다."
        )
        # 2. 인증서에서 사용자 선택 클릭
        self.click_ui_element(
            image_path='./images/user.png',
            grayscale=True,
            sleep_after=2,
            error_message="사용자를 찾을 수 없습니다."
        )

    def run(self):
        """
        전체 자동화 프로세스를 순서대로 실행합니다.
        각 단계에서 발생한 예외는 상위로 전달됩니다.
        """
        self.launch_program()
        self.perform_login()
        log.info("모든 작업 완료. 자동화 프로세스 종료.")

def main():
    automation = AutomationProcess()
    automation.run()

if __name__ == "__main__":
    try:
        log.info("------------------------------------------------------")
        log.info("프로그램 시작")
        log.info("------------------------------------------------------")
        main()
    except Exception as e:
        # 예외 발생 시 에러 메시지 기록
        log.error("프로그램 실행 중 예외 발생: %s", e)
        # 현재 화면 캡쳐하여 파일로 저장 (파일명에 타임스탬프 추가)
        screenshot_filename = f"screenshot_{int(time.time())}.png"
        pyautogui.screenshot(screenshot_filename)
        log.info("현재 화면이 %s에 저장되었습니다.", screenshot_filename)
        sys.exit(1)
    finally:
        log.info("------------------------------------------------------")
        log.info("프로그램 종료")
        log.info("------------------------------------------------------")

```
