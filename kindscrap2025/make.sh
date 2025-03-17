#!/bin/bash

# 1. settings.py에서 VERSION 값을 읽어오기
VERSION=$(grep -oP "self.VERSION\s*=\s*'\K[^']+" settings.py)

# 2. 실행 파일 이름 설정
EXE_NAME="kindscrap_${VERSION}.exe"

# 3. 기존 빌드 폴더 삭제
rm -rf dist/ build/

# 4. 실행 파일 생성
pyinstaller --onefile --name="$EXE_NAME" main.py

# 5. $HOME/bin으로 실행 파일 복사
mkdir -p "$HOME/bin"
cp "dist/$EXE_NAME" "$HOME/bin/"

# 6. 완료 메시지 출력
echo "✅ 빌드 완료: $HOME/bin/$EXE_NAME"
