# auto_esafe 사용자 매뉴얼

## 개요

esafe 2019 프로그램을 자동으로 수행시켜서 필요한 파일들을 다운로드 후  ftp 서버에 올리는 자돟으로 수행시킴

## 준비

1. 모니터의 디스플레이 속성이 1920x1080, 100%배열, 가로방향이어야 함
![디스플레이 속성](./images/display.png)

2. 공인인증서 : 구윤진님의 공인인증서가 하드디스크에 설치되어 있어야 함.
3. eSAFE2019.exe 가 PC에 있어야 함

## 설치 및 실행

1. 특정 폴더에 auto_esafe.exe와 .env 2개의 파일을 copy
2. 특정 폴더를 c:\auto_esafe 로 가정
3. .env를 환경에 맞게 수정 (hotepad 이용)
   1. PROGRAM_PATH <수정필요>
   2. SAVE_AS_PATH1 <수정필요>
4. win+r cmd
5. cd \auto_esafe
6. auto_esafe_$VERSION.exe

## 동작

auto_esafe는 다음과 같은 과정을 거치며 동작합니다.

1. pre_check : 화면 모니터, 필요한 파일들의 존재 여부 등 체크
2. holiday_check: 휴일에는 동작하지 않습니다.
3. 기존파일들 삭제: 오늘의 날짜로 되어 있는파일들 삭제
4. eSafe2019실행 및 파일 다운로드
5. 다운로드한 파일들을 csv로 변환
6. csv로 변환된 파일들을 sftp서버로 전송

## 스케줄링

1. taskschd.msc 에 특정시간에 자동으로 수행되게 함.
2. 동작
   1. 모니터를 깨움
   2. 수행
   3. 모니터 절전모드로 진입
