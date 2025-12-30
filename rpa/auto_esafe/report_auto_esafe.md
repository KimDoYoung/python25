# auto_esafe 프로젝트 보고서

## 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [프로젝트 목적](#프로젝트-목적)
3. [주요 기능](#주요-기능)
4. [시스템 구조](#시스템-구조)
5. [핵심 모듈](#핵심-모듈)
6. [의존성 및 필수 환경](#의존성-및-필수-환경)
7. [설정 관리](#설정-관리)
8. [데이터 처리 흐름](#데이터-처리-흐름)
9. [파일 전송 방식](#파일-전송-방식)
10. [배포 및 운영](#배포-및-운영)
11. [버전 정보](#버전-정보)
12. [개발 환경 및 빌드 프로세스](#개발-환경-및-빌드-프로세스)

---

## 프로젝트 개요

**프로젝트명**: auto_esafe  
**버전**: 1.1.4  
**언어**: Python  
**개발기간**: 2025년 2월 6일 ~ 2025년 2월 13일
**배포 형태**: PyInstaller를 이용한 Windows EXE 파일  
**성격**: RPA(Robotic Process Automation) 자동화 프로그램

### 설명

`auto_esafe`는 eSAFE2019 프로그램을 자동으로 제어하여 공인인증서 기반 로그인, 데이터 조회 및 다운로드, 파일 변환, 그리고 FTP/SFTP 서버로의 자동 전송을 수행하는 완전 자동화된 RPA 솔루션입니다.

---

## 프로젝트 목적

1. **자동화**: eSAFE2019의 반복적인 수동 작업을 완전히 자동화
2. **효율성**: 정해진 시간에 자동으로 데이터 수집 및 전송
3. **안정성**: 공인인증서 기반 보안 로그인 및 데이터 보호
4. **확장성**: 여러 조회 화면(500068, 500038, 800008, 800100)에 대응

---

## 주요 기능

### 1. eSAFE2019 자동 제어

- eSAFE2019 프로그램 실행
- 공인인증서를 이용한 자동 로그인
- 화면 크기 FHD(1920x1080) 기준으로 최적화

### 2. 4가지 데이터 조회 시나리오

| 화면번호 | 탭 | 파일형식 | 파일 개수 | 특이사항 |
|---------|-----|--------|---------|---------|
| 500068 | Tab1, Tab2 | CSV + Excel | 3개 | 오후 작업 모드(`pm` 인자) 지원 |
| 500038 | Tab1 | Excel | 1개 | 조회일: 전영업일 기준 |
| 800008 | - | Excel | 1개 | 증권구분 설정 필요, 설립일/발행 범위 설정 |
| 800100 | - | CSV | 1개 | 조건 없이 전체 조회 |

### 3. 파일 처리

- Excel 파일을 CSV 형식으로 자동 변환
- 한글 인코딩 지원 (CP949)
- 파일명에 날짜 자동 추가

### 4. 서버 전송

- **FTP** 또는 **SFTP** 방식 지원
- 변환된 파일 자동 업로드
- 전송 결과 로깅

### 5. 공휴일 처리

- 공공데이터 API 활용 공휴일 조회
- 전영업일 자동 계산

### 6. 로깅 및 모니터링

- 일별 로그 파일 자동 생성 (`auto_esafe_YYYY_MM_DD.log`)
- 오류 발생 시 스크린샷 자동 저장
- 상세한 작업 로그 기록

---

## 시스템 구조

```
auto_esafe/
├── auto_esafe.py              # 메인 실행 파일
├── config.py                  # 환경 설정 및 상수 관리
├── logger.py                  # 로깅 모듈
├── path_utils.py              # 경로 관리
├── rpa_utils.py               # RPA 유틸리티 함수
├── rpa_process.py             # 프로세스 관리
├── rpa_exceptions.py          # 예외 처리
├── rpa_misc.py                # 기타 유틸리티
├── excel_utils.py             # 엑셀/CSV 변환
├── working_days.py            # 공휴일 및 영업일 계산
├── .env                       # 환경 변수 (보안 정보)
├── requirements.txt           # Python 의존성
├── auto_esafe.spec            # PyInstaller 스펙
├── run_auto_esafe.bat         # Windows 배치 파일
├── make.sh                    # Linux/Git Bash 빌드 스크립트
├── README.md                  # 기본 설명서
└── doc/
    ├── user_manual.md         # 사용자 설명서
    └── images/                # 설명서 이미지
```

---

## 핵심 모듈

### 1. **auto_esafe.py** (메인 모듈)

- 프로그램 전체 흐름 제어
- eSAFE2019 자동 제어 (PyAutoGUI 사용)
- 화면 이미지 인식 및 작업 흐름 자동화
- FTP/SFTP 업로드 함수 포함

### 2. **config.py** (설정 관리)

- 모든 환경 변수 중앙화
- FTP/SFTP 접속 정보
- 경로 및 상수 정의
- 로깅 레벨 설정

### 3. **rpa_utils.py** (RPA 유틸리티)

- 화면 영역 계산 (`RegionName` Enum)
- 이미지 대기 및 찾기 함수
- 관리자 권한 확인
- 마우스/키보드 자동 조작

### 4. **excel_utils.py** (엑셀 처리)

- XLSX를 CSV로 변환 (`xlsx_to_csv()`)
- openpyxl 사용 (pandas 불필요)
- 한글 인코딩 지원

### 5. **working_days.py** (공휴일 계산)

- 공공데이터 API를 통한 공휴일 조회
- 전영업일 자동 계산 (`get_prev_working_day()`)
- 현재 날짜 처리

### 6. **rpa_process.py** (프로세스 관리)

- 프로세스 실행 상태 확인
- 프로세스 강제 종료
- 창 제목 조회

### 7. **logger.py** (로깅)

- 일별 로그 파일 생성
- 다양한 로그 레벨 지원
- 오류 시 스크린샷 자동 저장

### 8. **path_utils.py** (경로 관리)

- 상대 경로 계산
- .env 파일 위치
- 이미지 경로 관리

---

## 의존성 및 필수 환경

### Python 라이브러리

| 라이브러리 | 용도 |
|-----------|------|
| `pyautogui` | 화면 자동 제어, 마우스/키보드 조작 |
| `opencv-python` | 이미지 인식 및 화면 검색 |
| `psutil` | 프로세스 관리 |
| `python-dotenv` | .env 파일 환경 변수 로딩 |
| `screeninfo` | 모니터 정보 조회 |
| `pywin32` | Windows API 접근 |
| `requests` | HTTP 요청 (공휴일 API) |
| `pandas` | 데이터 처리 |
| `xlrd` | 엑셀 읽기 |
| `openpyxl` | XLSX 파일 처리 |
| `keyboard` | 키보드 입력 감지 |
| `paramiko` | SFTP 연결 |
| `Pillow` | 이미지 처리 (스크린샷) |

### 시스템 요구사항

| 항목 | 사양 |
|------|------|
| OS | Windows |
| 모니터 해상도 | FHD (1920x1080) 필수 |
| eSAFE2019 | 설치 필수 |
| 공인인증서 | 하드드라이브에 저장된 상태 |
| 관리자 권한 | 필요 |

---

## 설정 관리

### .env 파일 구조

```env
# 프로그램 설정
PROGRAM_PATH=C:\Program Files\eSAFE2019\esafe.exe
PROCESS_NAME=esafe.exe
WINDOWN_TITLE=eSAFE2019

# 로그 설정
LOG_LEVEL=INFO
SAVE_AS_PATH1=C:\temp

# 보안 정보
CERTI_LOCATION=D:\certificate
CERTI_USERNAME=사용자이름
CERTI_PASSWORD=인증서비밀번호

# SFTP 설정
SFTP_HOST=192.168.1.100
SFTP_PORT=22
SFTP_USER=ftp_user
SFTP_PASS=ftp_password
SFTP_REMOTE_DIR=/HDD1/esafe

# 공휴일 API
GODATA_API_KEY=your_api_key
HOLIDAY_FILE=holiday.json
```

### config.py의 주요 상수

- `VERSION`: 프로그램 버전
- `LOG_DIR`: 로그 저장 경로
- `LOG_FILE_FORMAT`: 로그 파일명 형식

---

## 데이터 처리 흐름

```
1. 프로그램 시작
   ↓
2. eSAFE2019 실행
   ↓
3. 공인인증서로 자동 로그인
   ↓
4. 화면별 데이터 조회
   ├─ 500068 (Tab1, Tab2)
   ├─ 500038 (Tab1)
   ├─ 800008 (Excel)
   └─ 800100 (CSV)
   ↓
5. 파일 다운로드
   ├─ 임시 폴더에 저장
   └─ Excel → CSV 변환
   ↓
6. eSAFE2019 종료
   ↓
7. FTP/SFTP 서버에 업로드
   ├─ 파일명: 날짜_화면번호_탭정보.확장자
   └─ 전송 성공 여부 로깅
   ↓
8. 프로그램 종료
```

---

## 파일 전송 방식

### FTP 방식

```python
def ftp_upload_files(filenames):
    # FTP_HOST, FTP_USER, FTP_PASS를 사용한 FTP 연결
    # FTP_REMOTE_DIR에 파일 업로드
```

### SFTP 방식

```python
def sftp_upload_files(filenames):
    # SFTP_HOST, SFTP_PORT를 사용한 SFTP 연결
    # Paramiko 라이브러리를 통한 안전한 연결
    # SFTP_REMOTE_DIR에 파일 업로드
```

---

## 배포 및 운영

### Windows Task Scheduler 설정

1. **작업 스케줄러 열기**
   - Windows + R → `taskschd.msc` 입력

2. **기본 작업 생성**
   - 작업명: `auto_esafe`
   - 트리거: 매일 정해진 시간
   - 작업: `auto_esafe.exe` 실행

3. **주요 설정**
   - ✅ **대기 모드 해제**: 예약된 작업이 대기 모드를 깨우도록 설정
   - ✅ **모니터 유지**: 디스플레이를 항상 활성화
   - ✅ **절전 모드 비활성화**: 전원 옵션에서 절전 비활성화

### 필수 Windows 설정

```
설정 → 시스템 → 디스플레이 → 고급 디스플레이 설정
- 디스플레이 끄기: 안 함

설정 → 시스템 → 전원 및 절전
- 절전 모드: 안 함

전원 옵션 → 고급 전원 설정
- Wake Timers 사용 설정
```

### 실행 시 주의사항

- ⚠️ **모니터 켜짐 상태 필수**: 프로그램 실행 중 모니터가 반드시 켜져 있어야 함
- ⚠️ **마우스 움직임 금지**: 자동화 작업 중 마우스를 움직이면 안 됨
- ⚠️ **해상도 고정**: FHD(1920x1080) 고정 필수

---

## 버전 정보

### 현재 버전: 1.1.4

### 주요 업데이트 히스토리

| 버전 | 날짜 | 주요 변경사항 |
|------|------|-------------|
| v1.0.3 | - | 사용자명으로 이미지를 내부에서 생성하여 비교 |
| v1.0.4 | - | 인증서 위치를 클릭하도록 수정 |
| v1.0.5 | - | 느린 PC에서도 조회 가능하도록 조회 시간을 최대 10분으로 확대 |
| v1.0.6 | - | 일부 이미지 grayscale 처리 |
| v1.0.7 | - | save path 오류 수정 |
| v1.0.8 | - | 500068 화면 추가 |
| v1.0.9 | - | FTP에서 SFTP로 변경 |
| v1.1.0 | - | 새로운 노트북에서 빌드, 대기시간 증가 |
| v1.1.1 | - | `pm` 모드 적용 (오후 작업 지원) |
| v1.1.2 | - | 오후작업에도 500086N.xls.csv 파일 추가 |
| v1.1.3 | 2025.11.13 | 500874 화면 추가 (외국납부세액조회), Excel 다운로드 지원 |
| v1.1.4 | 2025.12.15 | 3번째 인자로 화면번호, 4번째 인자로 날짜 지정 기능 추가 |

---

## 개발 환경 및 빌드 프로세스

### 개발 환경 구성

```bash
# 1. Git 클론
git clone <repository_url>

# 2. 가상환경 생성
python -m venv env

# 3. 가상환경 활성화
# Windows
env\Scripts\activate
# Git Bash / Linux
source env/Scripts/activate

# 4. 의존성 설치
pip install -r requirements.txt
```

### 버전 업데이트 절차

1. `config.py`의 `VERSION` 값 변경
2. 소스 코드 수정
3. 테스트 진행

### EXE 빌드 프로세스

```bash
# 가상환경 활성화 상태에서 실행
source env/Scripts/activate

# 기존 빌드 제거
rm -rf ./dist ./build

# PyInstaller로 EXE 생성
pyinstaller auto_esafe.spec
```

### PyInstaller 스펙 파일

- `auto_esafe.spec`: 기본 spec
- `auto_esafe_internal.spec`: 내부용 spec
- `auto_esafe.spec1`: 대체 spec

### 빌드 스크립트

- `make.sh`: Unix/Git Bash용 빌드 스크립트
- `run_auto_esafe.bat`: Windows 실행 배치 파일

---

## 부록: 주요 함수 목록

### auto_esafe.py

- `exception_handler(error_message)`: 예외 발생 시 스크린샷 및 로깅
- `ftp_upload_files(filenames)`: FTP 업로드
- `sftp_upload_files(filenames)`: SFTP 업로드

### excel_utils.py

- `xlsx_to_csv(xlsx_file, csv_file, sheet_name)`: Excel → CSV 변환
- `excel_to_csv()`: 전체 Excel → CSV 변환 처리

### working_days.py

- `get_prev_working_day(date)`: 전영업일 계산
- `get_today()`: 현재 날짜 반환
- `isHoliday(date)`: 공휴일 판단
- `todayYmd()`: 현재 날짜를 YYYYMMDD 형식으로 반환

### rpa_utils.py

- `get_region(base_region, region_name)`: 화면 영역 계산
- `is_admin()`: 관리자 권한 확인
- `wait_for_image(image_path, timeout)`: 이미지 대기
- `find_for_image(image_path)`: 화면에서 이미지 찾기
- `get_point_in_region(location, offset)`: 영역 내 좌표 계산

### rpa_process.py

- `list_running_programs()`: 실행 중인 프로세스 목록
- `is_process_running(program_name)`: 프로세스 실행 여부 확인
- `kill_process(process_name)`: 프로세스 종료
- `get_window_title_by_process(process_name)`: 창 제목 조회

---

## 결론

`auto_esafe`는 Python RPA 기술을 활용하여 Windows 환경에서 금융 데이터 수집을 완전히 자동화한 프로젝트입니다. PyAutoGUI를 통한 화면 제어, 이미지 인식, 파일 처리, 그리고 안전한 파일 전송을 통해 일관된 자동화 워크플로우를 제공합니다. 정기적인 버전 관리와 철저한 로깅을 통해 운영 안정성을 확보하고 있습니다.
