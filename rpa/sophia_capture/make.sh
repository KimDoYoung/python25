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

# 빌드 완료 메시지
if [ -f "dist/sophia.exe" ]; then
    echo "✅ 빌드 완료: dist/sophia.exe"
    cp dist/sophia.exe $HOME/bin/sophia.exe
    
else
    echo "❌ 빌드 실패!"
fi
