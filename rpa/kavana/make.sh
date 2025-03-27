#!/bin/bash

# 사용: ./make.sh [onefile|onedir]
MODE=${1:-onedir}  # ✅ 기본은 onedir

APP_NAME="kavana"
VENV_DIR="$(pwd)/venv"
PYTHON_PATH=$(which python)

# 가상환경 활성화
if [[ "$PYTHON_PATH" == *"venv/Scripts/python"* || "$PYTHON_PATH" == *"venv/bin/python"* ]]; then
    echo "🔄 이미 가상 환경이 활성화되어 있습니다: $PYTHON_PATH"
else
    if [ -d "$VENV_DIR" ]; then
        echo "🐍 가상 환경 활성화: $VENV_DIR"
        source "$VENV_DIR/Scripts/activate" 2>/dev/null || source "$VENV_DIR/bin/activate"
    else
        echo "❌ 가상 환경을 찾을 수 없습니다: $VENV_DIR"
        exit 1
    fi
fi

# PyInstaller 확인
PYINSTALLER_PATH=$(which pyinstaller)
if [[ "$PYINSTALLER_PATH" != "$VENV_DIR"* ]]; then
    echo "❌ PyInstaller가 가상 환경 내에 설치되어 있지 않습니다."
    echo "   → pip install pyinstaller"
    echo "   현재 pyinstaller 위치: $PYINSTALLER_PATH"
    exit 1
fi

# 설치 위치
INSTALL_DIR="$HOME/bin"

# 정리
echo "🧹 기존 빌드 파일 및 설치 디렉토리 삭제..."
rm -rf build/ dist/ logs/
rm -rf "$INSTALL_DIR/$APP_NAME"

# 빌드
echo "🚀 PyInstaller 빌드 시작 (모드: $MODE)..."

if [[ "$MODE" == "onedir" ]]; then
    pyinstaller --noconfirm --clean --onedir \
      --distpath "$INSTALL_DIR" \
      --name "$APP_NAME" "${APP_NAME}.py"
else
    TMPDIR="$HOME/.${APP_NAME}_tmp"
    pyinstaller --noconfirm --clean --onefile \
      --runtime-tmpdir "$TMPDIR" \
      --distpath "$INSTALL_DIR" \
      --name "$APP_NAME" "${APP_NAME}.py"
fi

# 결과 확인
if [[ "$MODE" == "onedir" ]]; then
    TARGET_EXE="$INSTALL_DIR/$APP_NAME/$APP_NAME.exe"
else
    TARGET_EXE="$INSTALL_DIR/$APP_NAME.exe"
fi
if [ ! -f "$TARGET_EXE" ]; then
    echo "❌ 빌드 실패: 실행 파일이 없습니다 → $TARGET_EXE"
    exit 1
fi

chmod +x "$TARGET_EXE"
echo "✅ 빌드 완료: $TARGET_EXE"
echo "📂 전체 실행 환경: $INSTALL_DIR"
echo "💡 실행하려면 다음 중 하나 사용:"
echo "   👉 $TARGET_EXE"
echo "   👉 export PATH=\$HOME/bin/$APP_NAME:\$PATH && $APP_NAME.exe"
