@echo off
SET EXE_PATH=C:\auto_esafe\auto_esafe.exe
SET DOWNLOAD_PATH=C:\auto_esafe\download
SET MAX_RETRIES=3
SET COUNT=0

:: 현재 날짜 가져오기 (YYYYMMDD 형식)
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value ^| find "="') do set DATETIME=%%I
set TODAY=%DATETIME:~0,8%

:: 파일 목록 설정 (절대 경로 사용)
SET FILE1=%DOWNLOAD_PATH%\%TODAY%_500068_T1.csv
SET FILE2=%DOWNLOAD_PATH%\%TODAY%_500068_T2.xls.csv
SET FILE3=%DOWNLOAD_PATH%\%TODAY%_500038.xls.csv
SET FILE4=%DOWNLOAD_PATH%\%TODAY%_800008.xls.csv
SET FILE5=%DOWNLOAD_PATH%\%TODAY%_800100.csv
SET FILE6=%DOWNLOAD_PATH%\%TODAY%_500086.xls.csv

:RETRY
echo 실행 시도 %COUNT%...
start /wait %EXE_PATH%

:: 잠시 대기 (파일 생성 대기)
timeout /t 5 /nobreak >nul

:: 파일이 모두 생성되었는지 확인
IF EXIST %FILE1% IF EXIST %FILE2% IF EXIST %FILE3% IF EXIST %FILE4% IF EXIST %FILE5% IF EXIST %FILE6% (
    echo 모든 파일이 정상적으로 생성되었습니다.
    exit /b 0
) ELSE (
    echo 파일이 누락되었습니다. 재시도 중...
)

:: 최대 재시도 횟수 확인
SET /A COUNT+=1
IF %COUNT% LSS %MAX_RETRIES% (
    goto RETRY
) ELSE (
    echo 최대 재시도 횟수를 초과했습니다. 프로그램을 종료합니다.
    exit /b 1
)
