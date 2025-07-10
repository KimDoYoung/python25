#!/usr/bin/env bash
# make.sh  ─ bash ./make.sh
# 1) uv로 가상환경(.venv) 생성
# 2) PyInstaller + python-dotenv 설치
# 3) .env를 실행파일에 포함 → dist/holiday.exe

set -euo pipefail

APP_NAME="holiday"        # holiday.exe
ENTRY="main.py"
VENV=".venv"              # uv가 기본으로 쓰는 이름이라 유지

########################################
# .env → 현재 셸(빌드 시)로 내보내기
########################################
if [[ -f .env ]]; then
  set -a
  # 주석/공백 제거 후 export
  source <(grep -vE '^\s*#' .env | grep -vE '^\s*$' | xargs -d '\n' -I{} echo {})
  set +a
fi

########################################
# 1) uv 기반 가상환경 준비
########################################
# 필요 시 uv 설치: curl -LsSf https://astral.sh/uv/install.sh | sh
# uv venv "$VENV"                 # .venv 생성·재사용 :contentReference[oaicite:0]{index=0}
# # 패키지 설치 (pip ↔ uv pip)
# uv pip install pyinstaller python-dotenv :contentReference[oaicite:1]{index=1}

########################################
# 2) 빌드 (uv run으로 툴 실행)
########################################
# OS별 --add-data 구분자(; ↔ :)
SEP=":"
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) SEP=";" ;;
esac

uv run pyinstaller \
  --clean \
  --onefile \
  --name "$APP_NAME" \
  --add-data ".env${SEP}." \
  "$ENTRY"

echo -e "\n✅  빌드 완료 → dist/${APP_NAME}.exe"

########################################
# 3) 유의 사항
########################################
# ▸ PyInstaller가 uv 자체 Python(Emscripten 빌드)와 맞지 않는 버전이
#   존재합니다. 문제가 생기면:
#     ── uv venv --python $(which python)  # 시스템 Python으로 venv 생성
#     ── 또는 pyinstaller==<호환버전> 지정
#   (참고: PyInstaller/uv 호환 이슈) :contentReference[oaicite:2]{index=2}
