#!/bin/bash

# 1. 기존 빌드 폴더 삭제
echo ">>> 기존 빌드 폴더 삭제 중..."
rm -rf ./dist ./build

# 2. config.py에서 VERSION 값을 추출
echo ">>> config.py에서 버전 정보 추출..."
VERSION=$(grep 'VERSION =' config.py | cut -d '"' -f2)
echo "🔹 추출된 버전: $VERSION"

# 3. auto_esafe.spec의 EXE 이름 수정
echo ">>> auto_esafe.spec 수정 중..."
sed -i "s/name='auto_esafe_[0-9.]*'/name='auto_esafe_$VERSION'/" auto_esafe.spec

# 4. PyInstaller 빌드 실행
echo ">>> PyInstaller 실행 중..."
pyinstaller --clean auto_esafe.spec

# 5. C:/tmp/auto_esafe 폴더 정리
TARGET_DIR="/c/tmp/auto_esafe"
echo ">>> $TARGET_DIR 내부 파일 삭제 중..."
rm -rf "$TARGET_DIR"/*
mkdir -p "$TARGET_DIR"

# 6. 생성된 exe 파일 복사
echo ">>> 빌드된 실행 파일 복사 중..."
cp "./dist/auto_esafe_$VERSION.exe" "$TARGET_DIR/"

# 7. 현재 폴더의 .env 파일 복사
echo ">>> .env 파일 복사 중..."
cp ".env" "$TARGET_DIR/"

# 8. doc 폴더의 user_manual.pdf 복사 (버전 추가)
echo ">>> user_manual.pdf 복사 중..."
cp "./doc/user_manual.pdf" "$TARGET_DIR/user_manual_$VERSION.pdf"

# 9. run_auto_esafe.bat의 VERSION 값 자동 변경
echo ">>> run_auto_esafe.bat 파일 수정 및 복사 중..."

# VERSION 값 치환 후 CP949(ASCII)로 변환하여 저장
sed "s/^set VERSION=.*/set VERSION=$VERSION/" run_auto_esafe.bat | iconv -f UTF-8 -t CP949 > "$TARGET_DIR/run_auto_esafe.bat"

echo "-----------------------------"
echo "✅ 빌드 및 배포 완료!!!"
echo "$TARGET_DIR 폴더를 확인하세요"
echo "-----------------------------"
