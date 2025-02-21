import subprocess

def run_kavana_script(script_path):
    """
    Kavana 스크립트를 실행하고 출력 결과를 반환한다.
    """
    result = subprocess.run(
        ["python", "kavana.py", script_path],
        capture_output=True, text=True, encoding="utf-8"  # ✅ 인코딩을 UTF-8로 지정
    )
    return result.stdout.strip()  # 출력 결과 반환

def test_kavana_script():
    """
    0.kvs 스크립트 실행 결과가 예상 출력과 일치하는지 검증.
    """
    script_path = "./scripts/0.kvs"
    expected_output = "hello"

    output = run_kavana_script(script_path)
    assert output == expected_output, f"출력 불일치! 예상: {expected_output}, 실제: {output}"
