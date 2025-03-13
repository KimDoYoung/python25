#!/bin/bash

# 가상 환경 경로 (프로젝트에 맞게 수정)
VENV_DIR="$(pwd)/venv"

# 가상 환경 활성화
if [ -d "$VENV_DIR" ]; then
    echo "🐍 가상 환경 활성화: $VENV_DIR"
    source "$VENV_DIR/bin/activate"
else
    echo "❌ 가상 환경을 찾을 수 없습니다: $VENV_DIR"
    exit 1
fi

# 설정: 실행 파일을 저장할 디렉토리
INSTALL_DIR="$HOME/bin"

# 빌드 디렉토리 정리
echo "🛠 기존 빌드 파일 삭제..."
rm -rf build/ dist/ kavana.exe

# PyInstaller를 사용하여 실행 파일 빌드
echo "🚀 PyInstaller로 kavana.exe 빌드 중..."
pyinstaller kavana.spec

# 빌드 성공 확인
if [ ! -f "dist/kavana.exe" ]; then
    echo "❌ 빌드 실패: dist/kavana.exe가 없습니다."
    exit 1
fi

# 실행 파일을 $HOME/bin으로 이동 (폴더 없으면 생성)
echo "📂 실행 파일을 $INSTALL_DIR 로 이동..."
mkdir -p "$INSTALL_DIR"
mv dist/kavana.exe "$INSTALL_DIR/"

# 권한 설정 (실행 가능하도록)
chmod +x "$INSTALL_DIR/kavana.exe"

echo "✅ 빌드 완료! 이제 터미널에서 'kavana a.kvs' 실행 가능."

# 가상 환경 비활성화
deactivate
