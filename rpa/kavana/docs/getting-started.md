# 시작하기(Getting-Started)

kavana script에 관심을 갖어주셔서 감사합니다.
kavana는 [RPA (Robotic Process Automation)](https://namu.wiki/w/RPA) 에 특화된 DSL(도메인특화언어:Domain-Specific Language)이라고 할 수 있읍니다.
python언어로 작성되었으며 실제로 동작하기 위해서는 exe로 빌드해서 path에 등록해 두어야 합니다.

## 1. 필수사항

- Python 3.10+
- Git
- pip (Python package manager)

## 2. 설치

- 개발환경 : python 3.12.1
- 터미널 : git bash

```bash
python --version
git clone https://github.com/username/mycoolproject.git
cd mycoolproject
python -m venv venv
which python
pip install -r requirements.txt
which pyinstaller
./make.sh
```

- make.sh 은 pyinstaller를 실행합니다
