@echo off
setlocal enabledelayedexpansion
cd /d %~dp0

:: 실행 파일 및 설정
set EXE_NAME=kindscrap_1.4.exe
set MAX_RETRIES=3
set RETRY_COUNT=0

:: 기본값 설정 (어제 날짜 구하기)
for /f "tokens=2 delims==" %%I in ('"wmic os get localdatetime /value"') do set DATETIME=%%I
set YEAR=%DATETIME:~0,4%
set MONTH=%DATETIME:~4,2%
set DAY=%DATETIME:~6,2%

:: 어제 날짜 계산 (PowerShell 사용)
for /f %%i in ('powershell -command "(Get-Date).AddDays(-1).ToString('yyyy-MM-dd')"') do set YESTERDAY=%%i

:: 인자 설정 (입력값이 없으면 어제 날짜 사용)
set ARG1=%1
set ARG2=%2
set ARG3=%3

if "%ARG1%"=="" set ARG1=%YESTERDAY%
if "%ARG2%"=="" set ARG2=%YESTERDAY%
if "%ARG3%"=="" set ARG3=all

:RUN_PROCESS
set /a RETRY_COUNT+=1
echo ======================================================
echo [%RETRY_COUNT%회차 실행] %EXE_NAME% %ARG1% %ARG2% %ARG3%
echo 실행 시간: %date% %time%
echo ======================================================

:: [중요] 실행 전 잔여 크롬 프로세스 정리
:: 이전 실패로 인해 남은 드라이버나 브라우저를 강제 종료합니다.
taskkill /f /im chrome.exe /t >nul 2>&1
taskkill /f /im chromedriver.exe /t >nul 2>&1

:: 프로그램 실행
"%EXE_NAME%" %ARG1% %ARG2% %ARG3%
set EXIT_CODE=%ERRORLEVEL%

:: 성공 시 종료
if "%EXIT_CODE%"=="0" (
    echo.
    echo ✅ 작업이 성공적으로 완료되었습니다.
    goto END
)

:: 실패 시 재시도 로직
if %RETRY_COUNT% LSS %MAX_RETRIES% (
    echo.
    echo ❌ 작업 실패 (Exit Code: %EXIT_CODE%)
    echo 10초 후 재시도를 시작합니다... (%RETRY_COUNT%/%MAX_RETRIES%)
    timeout /t 10 /nobreak
    goto RUN_PROCESS
) else (
    echo.
    echo 🛑 %MAX_RETRIES%회 재시도 후에도 실패하였습니다.
    echo 로그 파일(error1.txt)을 확인해 주세요.
    pause
    exit /b %EXIT_CODE%
)

:END
timeout /t 5
exit /b 0