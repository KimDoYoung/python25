@echo off

:: 관리자 권한 확인 및 상승 실행
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 관리자 권한이 필요합니다. 다시 실행합니다...
    exit
)

:: 기존 모니터 및 절전 시간 저장
for /f "tokens=2 delims=," %%a in ('powercfg /query SCHEME_CURRENT SUB_VIDEO VIDEOIDLE ^| findstr "Power Setting Index"') do set OLD_MONITOR=%%a
for /f "tokens=2 delims=," %%a in ('powercfg /query SCHEME_CURRENT SUB_SLEEP STANDBYIDLE ^| findstr "Power Setting Index"') do set OLD_STANDBY=%%a

echo 기존 모니터 타임아웃: %OLD_MONITOR%
echo 기존 절전 모드 타임아웃: %OLD_STANDBY%

:: 절전 모드 방지
powercfg /change monitor-timeout-ac 0
powercfg /change standby-timeout-ac 0

:: 버전 정보
set VERSION=1.0.9

:: 절전 모드 해제
powercfg /waketimers
if %errorlevel% neq 0 echo "절전 해제 타이머가 없습니다."

:: 10초 대기
timeout /t 10 /nobreak

:: auto_esafe 실행 후 종료될 때까지 대기
start /wait "" "C:\auto_esafe\auto_esafe_%VERSION%.exe"

:: 실행 완료 후 5분 대기
timeout /t 300 /nobreak

:: 절전 모드로 전환
rundll32.exe powrprof.dll,SetSuspendState Sleep

:: 원래 모니터 및 절전 시간 복원
powercfg /change monitor-timeout-ac %OLD_MONITOR%
powercfg /change standby-timeout-ac %OLD_STANDBY%
