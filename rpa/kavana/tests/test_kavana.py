import subprocess
import os

def run_kavana_script(script_path):
    """
    Kavana 스크립트를 실행하고 출력 결과를 반환한다.
    """
    result = subprocess.run(
        ["python", "kavana.py", script_path],
        capture_output=True, text=True, encoding="utf-8"  # ✅ UTF-8 인코딩 설정
    )
    return result.stdout.strip()  # 출력 결과 반환

def test_kavana_scripts():
    """
    scripts 디렉터리에 있는 여러 개의 Kavana 스크립트를 실행하고, 
    각각의 예상 출력과 일치하는지 확인한다.
    """
    test_cases = {
        1: ("hello",),  # ./scripts/0.kvs → "hello" 출력 예상
        2: ("hello", "", "123"),
        3: ("hello 홍길동")
    }

    for test_num, expected_outputs in test_cases.items():
        script_path = f"./scripts/{test_num}.kvs"
        
        if not os.path.exists(script_path):
            print(f"⚠️ 테스트 파일 없음: {script_path} (건너뜀)")
            continue

        output = run_kavana_script(script_path)
        expected_output = "\n".join(expected_outputs)

        assert output == expected_output, f"🚨 출력 불일치! 파일: {script_path}, 예상: {expected_output}, 실제: {output}"
