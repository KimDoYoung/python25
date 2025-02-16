#!/bin/bash

# 프로젝트 기본 디렉토리 설정
PROJECT_DIR=$(pwd)
VENV_DIR="venv"

echo "🔹 Python 프로젝트 초기화 스크립트 실행"

# .gitignore 파일 생성
echo "🔹 .gitignore 파일 생성"
cat <<EOF > .gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
venv/
env/


# macOS 관련
.DS_Store
EOF

# README.md 파일 생성
echo "🔹 README.md 파일 생성"
echo "# $(basename $PROJECT_DIR)" > README.md
echo -e "\n프로젝트 설명을 여기에 작성하세요." >> README.md

# .vscode 폴더 및 기본 설정 파일 생성
echo "🔹 VSCode 설정 파일 생성"
mkdir -p .vscode
cat <<EOF > .vscode/settings.json
{
    "python.defaultInterpreterPath": "\${workspaceFolder}/venv/bin/python",
    "editor.formatOnSave": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.testing.pytestEnabled": true
}
EOF

cat <<EOF > .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "\${file}",
            "console": "integratedTerminal"
        }
    ]
}
EOF

# 기본 폴더 구조 생성
echo "🔹 프로젝트 기본 폴더 구조 생성"
mkdir -p src tests docs

# requirements.txt 파일 생성
echo "🔹 requirements.txt 생성"
touch requirements.txt

# Python 가상환경 생성
echo "🔹 Python 가상환경 설정 ($VENV_DIR)"
python -m venv $VENV_DIR

# Git 초기화
#echo "🔹 Git 초기화"
#git init

# 완료 메시지
echo "✅ 프로젝트 초기화 완료!"
echo "🚀 실행 방법: 'source $VENV_DIR/bin/activate' (Mac/Linux) 또는 '$VENV_DIR\Scripts\activate' (Windows)"
