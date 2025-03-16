#!/bin/bash

# 1. package.json의 version 값을 1 증가
echo "Updating version in package.json..."
VERSION=$(grep -oP '"version": *"\K[0-9]+\.[0-9]+\.[0-9]+' package.json)  # 현재 버전 추출
IFS='.' read -r -a VERSION_PARTS <<< "$VERSION"
((VERSION_PARTS[2]++))  # 마지막 숫자(패치 버전) 증가
NEW_VERSION="${VERSION_PARTS[0]}.${VERSION_PARTS[1]}.${VERSION_PARTS[2]}"

# package.json에서 기존 버전 값을 새 버전으로 변경
sed -i.bak "s/\"version\": \"$VERSION\"/\"version\": \"$NEW_VERSION\"/" package.json
echo "New version: $NEW_VERSION"

# 2. vsce package 실행
echo "Building VS Code extension package..."
vsce package

# 3. 기존 설치된 확장 제거 (정확한 ID 사용)
EXTENSION_ID="kalpa-tech.kavana-script"
echo "Uninstalling existing extension: $EXTENSION_ID"
code --uninstall-extension $EXTENSION_ID

# 4. 새로 만들어진 .vsix 확장 설치
VSIX_FILE=$(ls -t *.vsix | head -n 1)  # 가장 최신의 vsix 파일 선택
if [ -n "$VSIX_FILE" ]; then
    echo "Installing new extension: $VSIX_FILE"
    code --install-extension "$VSIX_FILE"
else
    echo "Error: No .vsix file found!"
    exit 1
fi

echo "✅ Extension updated and installed successfully!"
