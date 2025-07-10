# service_example

## 개요
1. window service에 python 프로그램을 등록
2. app은 10분마다 무한 반복으로 main의 특정 task를 수행함.

## 수행
```bash
# 1) 서비스 설치
python src/service_wrapper.py install

# 2) 바로 시작
python src/service_wrapper.py start

# 3) 상태 확인
sc query SimplePrintService

# 4) 중지
python src/service_wrapper.py stop

# 5) 제거
python src/service_wrapper.py remove
```

# 설치
```
python -m pywin32_postinstall -install
```
4개의 파일을 .venv아래에
1. pythonservice.exe
2. python312.dll
3. pythoncom312.dll
4. pywintype312.dll
