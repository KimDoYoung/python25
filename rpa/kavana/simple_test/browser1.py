from lib.core.managers.browser_manager import BrowserManager

def run_browser_command(command, **kwargs):
    print(f"\n 실행: {command}")
    manager = BrowserManager(command=command, **kwargs)
    manager.execute()

def main():
    # 1. OPEN
    run_browser_command(
        command="OPEN",
        url="https://www.naver.com",
        headless=False,  # True로 하면 창이 뜨지 않음
        window_size="1200x800"
    )

    # 2. TYPE (검색어 입력)
    run_browser_command(
        command="TYPE",
        selector="#query",
        text="카바나",
        clear_before=True
    )

    # 3. CLICK (검색 버튼)
    run_browser_command(
        command="CLICK",
        selector=".btn_search"
    )

    # 4. WAIT (결과 영역이 보일 때까지)
    # run_browser_command(
    #     command="WAIT",
    #     selector=".list_news",  # 결과 목록이 나타날 때까지 대기
    #     until="visible",
    #     timeout=5
    # )

    # 5. SCREENSHOT 저장
    run_browser_command(
        command="CAPTURE",
        path="naver_search_result.png"
    )

    # 6. CLOSE
    run_browser_command(command="CLOSE")

if __name__ == "__main__":
    main()
