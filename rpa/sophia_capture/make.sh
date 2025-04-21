#!/bin/bash

# Sophia-Capture 빌드 스크립트
echo "🛠 Sophia-Capture 빌드 시작..."

# 기존 빌드 파일 삭제
echo "🗑 기존 빌드 파일 삭제..."
rm -rf build/ dist/ sophia.spec

# 아이콘 경로 (절대 경로 변환)
ICON_PATH=$(realpath src/sophia_capture.ico)

# PyInstaller 실행
echo "🚀 PyInstaller 실행..."
pyinstaller --noconsole --onefile --icon="$ICON_PATH" src/sophia.py

# 실행 파일 이름 설정
TARGET_NAME="sophia"
EXT=""

# OS에 따라 확장자 설정
case "$OSTYPE" in
  msys*|cygwin*|win32*)
    EXT=".exe"
    ;;
esac

OUTPUT_PATH="dist/${TARGET_NAME}${EXT}"

# 빌드 완료 메시지
if [ -f "$OUTPUT_PATH" ]; then
    echo "✅ 빌드 완료: $OUTPUT_PATH"
    mkdir -p "$HOME/bin"
    cp "$OUTPUT_PATH" "$HOME/bin/${TARGET_NAME}${EXT}"
else
    echo "❌ 빌드 실패!"
fi
