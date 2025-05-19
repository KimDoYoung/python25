#!/bin/bash

# PRG_NAME
PRG_NAME="kindscrap"

# 아래부분을 같아야한다
TODAY=$(date +"%Y-%m-%d")
YESTERDAY=$(date -d "-1 day" +"%Y-%m-%d")
SCRIPT_DIR="/asset-bat/batch/$PRG_NAME"
ENV_FILE="/asset-bat/batch/$PRG_NAME/.env.real"
DEFAULT_ENV_FILE="/asset-bat/.env.real"
MAIN_PY="$SCRIPT_DIR/main.py"

# 운영 체제 확인
OS_TYPE=$(uname)
echo "Operating System: $OS_TYPE"

# .env.real 강제 복사
cp "$DEFAULT_ENV_FILE" "$ENV_FILE"

# Python 스크립트 실행 및 로그 파일에 저장
if [[ "$OS_TYPE" == "Linux" || "$OS_TYPE" == "Darwin" ]]; then
    echo "Starting $PRG_NAME"
    python3 "$MAIN_PY" "$YESTERDAY" "$YESTERDAY" "all"
else
    echo "Unsupported Operating System: $OS_TYPE"
    exit 1
fi