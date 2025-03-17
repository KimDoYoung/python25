@echo off
cd /d %~dp0

:: 실행 파일 이름
set EXE_NAME=kindscrap_1.0.exe

:: 기본값 설정 (어제 날짜 구하기)
for /f "tokens=2 delims==" %%I in ('"wmic os get localdatetime /value"') do set DATETIME=%%I
set YEAR=%DATETIME:~0,4%
set MONTH=%DATETIME:~4,2%
set DAY=%DATETIME:~6,2%

:: 어제 날짜 계산 (PowerShell 사용)
for /f %%i in ('powershell -command "(Get-Date).AddDays(-1).ToString('yyyy-MM-dd')"') do set YESTERDAY=%%i

:: 인자가 없을 경우 기본값 사용
set ARG1=%1
set ARG2=%2
set ARG3=%3

if "%ARG1%"=="" set ARG1=%YESTERDAY%
if "%ARG2%"=="" set ARG2=%YESTERDAY%
if "%ARG3%"=="" set ARG3=all

:: 실행
echo running: %EXE_NAME% %ARG1% %ARG2% %ARG3%
"%EXE_NAME%" %ARG1% %ARG2% %ARG3%
