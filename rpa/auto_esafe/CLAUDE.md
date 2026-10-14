# auto_esafe - RPA 프로젝트 분석 문서

> 이 문서는 Claude AI가 프로젝트를 분석하여 작성한 문서입니다.
> 작성일: 2026-10-14
> 버전: 1.1.7

## 프로젝트 개요

**auto_esafe**는 eSAFE2019 금융 시스템을 자동으로 조작하여 데이터를 다운로드하고 SFTP 서버로 업로드하는 RPA(Robotic Process Automation) 솔루션입니다.

### 핵심 기능
- eSAFE2019 프로그램 자동 실행 및 공인인증서 로그인
- 다양한 화면번호의 데이터 자동 다운로드 (6개 화면)
- Excel 파일을 CSV로 자동 변환
- SFTP를 통한 파일 자동 업로드
- 공휴일 자동 확인 및 영업일 계산 (공공데이터 API 활용)
- Windows Task Scheduler를 통한 스케줄링 실행

---

## 프로젝트 구조

```
auto_esafe/
├── auto_esafe.py           # 메인 RPA 스크립트 (현재 버전)
├── auto_esafe117.py        # 최신 버전 (v1.1.7)
├── config.py               # 환경 설정 및 상수 관리
├── logger.py               # 로깅 시스템 (싱글톤)
├── working_days.py         # 영업일 계산 (공공데이터 API)
├── excel_utils.py          # Excel to CSV 변환
├── rpa_utils.py            # RPA 유틸리티 함수
├── rpa_process.py          # 프로세스 관리
├── rpa_exceptions.py       # 커스텀 예외 정의
├── rpa_misc.py             # 기타 유틸리티
├── path_utils.py           # 경로 관리 유틸리티
├── .env                    # 환경 변수 (비밀번호, 인증서 정보)
├── env.sample              # 환경 변수 템플릿
├── requirements.txt        # Python 패키지 의존성
├── auto_esafe.spec         # PyInstaller 빌드 설정
├── make.sh                 # 빌드 스크립트
├── run_auto_esafe.bat      # 실행 배치 파일
├── doc/
│   └── user_manual.md      # 사용자 매뉴얼
├── images/                 # 이미지 인식용 PNG 파일들
├── log/                    # 로그 파일 저장 (auto_esafe_YYYY_MM_DD.log)
├── dist/                   # 빌드된 실행 파일
└── build/                  # 빌드 임시 폴더
```

---

## 핵심 모듈 설명

### 1. auto_esafe117.py (메인 스크립트)
**라인 수**: 966줄
**역할**: RPA 자동화의 핵심 로직

#### 주요 함수

| 함수명 | 라인 | 설명 |
|--------|------|------|
| `work_start_main()` | 126-173 | eSAFE2019 실행, 로그인, 메인 화면 진입 |
| `work_500068_tab1()` | 176-233 | 기준가1 조회 및 다운로드 |
| `work_500068_tab2()` | 235-297 | 기준가2 조회 및 다운로드 |
| `work_500038()` | 299-365 | 분배금 내역통보 조회 (전영업일 ~ 어제) |
| `work_800008()` | 367-449 | 종목발행현황 조회 (-60일 ~ 오늘) |
| `work_800100()` | 451-490 | 일자별 일정현황 조회 |
| `work_500086()` | 492-540 | 등록잔량서비스 조회 |
| `work_500874()` | 543-608 | 외국 납부세액조회 |
| `esafe_auto_work()` | 696-765 | 오전 작업 전체 프로세스 |
| `esafe_auto_work_pm()` | 868-900 | 오후 작업 전체 프로세스 |
| `sftp_upload_files()` | 50-79 | SFTP를 통한 파일 업로드 |
| `pre_check()` | 638-666 | 실행 전 환경 검증 |

#### 작업 프로세스
1. **pre_check**: 환경 검증 (해상도, DPI, 파일 존재 여부)
2. **공휴일 체크**: 휴일이면 종료
3. **기존 파일 삭제**: 같은 날짜의 기존 파일 삭제
4. **eSAFE 실행 및 로그인**
5. **데이터 다운로드**: 6개 화면에서 데이터 추출
6. **CSV 변환**: Excel 파일을 CSV로 변환
7. **SFTP 업로드**: 변환된 파일을 서버로 전송

---

### 2. config.py (환경 설정)
**라인 수**: 63줄
**역할**: 환경 변수 및 상수 관리

#### 주요 설정 항목
```python
VERSION = "1.1.7"                    # 프로그램 버전
PROGRAM_PATH                         # eSAFE2019.exe 경로
PROCESS_NAME                         # 프로세스 이름
CERTI_LOCATION                       # 인증서 위치 (USB/HDD)
USERNAME, PASSWORD                   # 인증서 사용자명, 비밀번호
SAVE_AS_PATH1                        # 파일 저장 경로
SFTP_HOST, SFTP_PORT, SFTP_USER     # SFTP 서버 정보
GODATA_API_KEY                       # 공공데이터 API 키
HOLIDAY_FILE                         # 공휴일 로컬 파일 경로
LOG_LEVEL, LOG_DIR                   # 로그 설정
```

---

### 3. working_days.py (영업일 계산)
**라인 수**: 161줄
**역할**: 공공데이터 API를 활용한 영업일 계산

#### 주요 함수
| 함수명 | 라인 | 설명 |
|--------|------|------|
| `get_holiday_list()` | 11-43 | 공공데이터 API에서 공휴일 목록 조회 |
| `get_prev_working_day()` | 76-91 | 이전 영업일 계산 (주말, 공휴일 제외) |
| `get_prev_working_3day()` | 101-120 | 3영업일 전 날짜 계산 |
| `get_prev_2month_day()` | 93-99 | 2개월 전 날짜 계산 |
| `isHoliday()` | 148-161 | 특정 날짜가 공휴일인지 확인 |

#### 특징
- **Fallback 메커니즘**: API 오류 시 로컬 파일(HOLIDAY_FILE)에서 공휴일 정보 로드
- **에러 처리**: 네트워크 오류, 타임아웃, XML 파싱 에러 모두 처리

---

### 4. rpa_utils.py (RPA 유틸리티)
**라인 수**: 305줄
**역할**: 이미지 인식, 마우스/키보드 제어, 화면 영역 관리

#### 주요 클래스/함수
| 이름 | 라인 | 설명 |
|------|------|------|
| `RegionName` (Enum) | 34-47 | 화면 영역 정의 (LEFT_TOP, RIGHT_BOTTOM 등) |
| `Direction` (Enum) | 49-53 | 방향 정의 (RIGHT, LEFT, UP, DOWN) |
| `get_region()` | 82-117 | RegionName에 따른 화면 영역 계산 |
| `wait_for_image()` | 134-149 | 이미지가 화면에 나타날 때까지 대기 |
| `find_and_click()` | 173-183 | 이미지를 찾아 클릭 |
| `find_and_press_key()` | 185-204 | 이미지를 찾아 키 입력 |
| `put_keys()` | 265-305 | 문자열 기반 키 입력 자동화 |

#### 특징
- **이미지 인식**: pyautogui를 이용한 화면 요소 탐지
- **좌표 계산**: 화면을 9개 영역으로 분할하여 탐색 최적화
- **클립보드 활용**: 한글/특수문자 입력 시 pyperclip 사용

---

### 5. logger.py (로깅 시스템)
**라인 수**: 73줄
**역할**: 싱글톤 패턴 로거

#### 특징
- 파일과 콘솔에 동시 출력
- UTF-8 인코딩 지원
- 날짜별 로그 파일 생성 (`auto_esafe_YYYY_MM_DD.log`)
- 이모지 기반 로그 레벨 표시 (🐛 DEBUG, ℹ️ INFO, ⚠️ WARNING, ❌ ERROR)

---

### 6. excel_utils.py (Excel 변환)
**라인 수**: 78줄
**역할**: Excel 파일을 CSV로 변환

#### 지원 형식
- `.xls` → xlrd 사용
- `.xlsx` → openpyxl 사용
- 인코딩: cp949 (Windows 환경 호환)

---

## 데이터 다운로드 화면 정보

| 화면번호 | 명칭 | 파일 형식 | 날짜 범위 | 파일명 패턴 |
|---------|------|---------|---------|----------|
| 500068 (Tab1) | 기준가1 | CSV | - | YYYYMMDD_500068_T1.csv |
| 500068 (Tab2) | 기준가2 | Excel→CSV | - | YYYYMMDD_500068_T2.xls.csv |
| 500038 | 분배금 내역통보 | Excel→CSV | 전영업일 ~ 어제 | YYYYMMDD_500038.xls.csv |
| 800008 | 종목발행현황 | Excel→CSV | 60일전 ~ 오늘 | YYYYMMDD_800008.xls.csv |
| 800100 | 일자별 일정현황 | CSV | - | YYYYMMDD_800100.csv |
| 500086 | 등록잔량서비스 | Excel→CSV | - | YYYYMMDD_500086.xls.csv |
| 500874 | 외국 납부세액조회 | Excel→CSV | - | YYYYMMDD_500874.xls.csv |

### 오후 작업 (mode="pm")
- 500068 신규등록 (T1N, T2N)
- 500086 오후 작업 (500086N)

---

## 기술 스택

### Python 패키지
```txt
pyautogui          # GUI 자동화
opencv-python      # 이미지 인식
psutil             # 프로세스 관리
python-dotenv      # 환경 변수 관리
screeninfo         # 화면 정보
pywin32            # Windows API
requests           # HTTP 통신 (공공데이터 API)
pandas, xlrd, openpyxl  # Excel 처리
keyboard           # 키보드 제어
paramiko           # SFTP 클라이언트
Pillow             # 이미지 처리
```

### 외부 API
- **공공데이터 포털**: 특일정보 조회 API (공휴일 정보)
  - URL: `https://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo`

---

## 환경 요구사항

### 필수 조건
1. **운영체제**: Windows (pywin32 의존성)
2. **화면 해상도**: 1920x1080 (FHD)
3. **DPI 설정**: 100% (스케일 팩터 1.0)
4. **화면 방향**: 가로
5. **eSAFE2019**: 설치 필수
6. **공인인증서**: HDD 또는 USB에 설치

### 실행 전 설정
1. `.env` 파일 작성 (env.sample 참고)
2. 로그 폴더: 자동 생성 (`log/`)
3. 저장 폴더: 자동 생성 (SAVE_AS_PATH1)

---

## 실행 방법

### 개발 환경
```bash
# 가상환경 생성 및 활성화
python -m venv env
source env/Scripts/activate

# 패키지 설치
pip install -r requirements.txt

# 실행
python auto_esafe117.py          # 오전 작업
python auto_esafe117.py pm       # 오후 작업
```

### 프로덕션 (EXE)
```bash
# 빌드
./make.sh

# 실행
./dist/auto_esafe.exe
./dist/auto_esafe.exe pm
```

### Windows Task Scheduler 설정
1. `Win + R` → `taskschd.msc`
2. 작업 생성: 매일 지정 시간에 실행
3. **중요**: 실행 시 모니터 켜져 있어야 함, 마우스 움직이지 말 것
4. 절전 모드 해제 필요

---

## 주요 설정 파일

### .env 예시
```env
PROGRAM_PATH=C:/Program Files/eSafe/eSAFE2019.exe
PROCESS_NAME=eSAFE2019.exe
WINDOWN_TITLE=eSAFE2019
SAVE_AS_PATH1=C:/auto_esafe/downloads

CERTI_LOCATION=HDD
CERTI_USERNAME=사용자명
CERTI_PASSWORD=비밀번호

SFTP_HOST=192.168.1.100
SFTP_PORT=22
SFTP_USER=ftpuser
SFTP_PASS=ftppass
SFTP_REMOTE_DIR=/HDD1/esafe

GODATA_API_KEY=공공데이터API키
HOLIDAY_FILE=C:/auto_esafe/holidays.txt

LOG_LEVEL=INFO
```

---

## 에러 처리

### 예외 타입
- `CertiError`: 인증서 오류 (사용자명/비밀번호 불일치)
- `HolidayError`: 공휴일 실행 시도

### 에러 발생 시 동작
1. 스크린샷 저장: `log/error_YYYY_MM_DD_HH_MM_SS.png`
2. 로그 기록: 에러 메시지 및 스택 트레이스
3. 프로세스 종료: eSAFE2019 강제 종료

---

## 버전 히스토리

| 버전 | 날짜 | 변경 사항 |
|------|------|----------|
| 1.0.3 | - | 사용자명 이미지 내부 생성 |
| 1.0.4 | - | 인증서 위치 클릭 기능 |
| 1.0.5 | - | 조회 시간 10분으로 확장 (느린 PC 대응) |
| 1.0.6 | - | 일부 이미지 grayscale 변환 |
| 1.0.7 | - | save path 오류 수정 |
| 1.0.8 | - | 500068 추가 |
| 1.0.9 | - | SFTP로 변경 |
| 1.1.0 | - | 새 노트북 빌드, 대기시간 조정 |
| 1.1.1 | - | mode pm 적용 |
| 1.1.2 | - | 오후 작업 500086N.xls.csv 추가 |
| 1.1.3 | 2025.11.13 | 500874(외국납부세액조회) 추가 |
| 1.1.4 | 2026.01.02 | 800008 위치 수정 |
| 1.1.5 | 2026.04.01 | 800008 종목등록일 -60일~오늘로 조정 |
| 1.1.6 | 2026.08.03 | 공공데이터 오류 시 프로그램 멈춤 버그 수정 |
| **1.1.7** | **2026.10.14** | **except 옵션 추가** |

---

## 주의 사항

1. **화면 해상도**: 반드시 1920x1080, 100% DPI
2. **실행 중 주의**: 마우스/키보드 사용 금지
3. **모니터 상태**: 항상 켜져 있어야 함 (절전 모드 해제)
4. **공인인증서**: 유효 기간 확인 필요
5. **공공데이터 API**: API 키 유효성 확인, 로컬 fallback 파일 준비
6. **백업**: 로그 파일 주기적 백업 권장

---

## 개발 가이드

### 새로운 화면 추가 방법
1. `images/` 폴더에 인식용 PNG 이미지 추가
2. `auto_esafe117.py`에 `work_[화면번호]()` 함수 작성
3. `esafe_auto_work()` 또는 `esafe_auto_work_pm()`에 함수 호출 추가
4. `config.py`의 VERSION 업데이트
5. `make.sh`로 빌드

### 빌드 프로세스
```bash
source env/Scripts/activate
which python
which pip
rm -rf ./dist ./build
pyinstaller auto_esafe.spec
```

### 디버깅 팁
- `LOG_LEVEL=DEBUG`로 설정하여 상세 로그 확인
- 에러 스크린샷 확인: `log/error_*.png`
- 이미지 인식 실패 시 confidence 값 조정 (기본 0.8)
- grayscale 옵션 활성화로 인식률 향상

---

## 보안 고려사항

1. **환경 변수**: `.env` 파일은 `.gitignore`에 포함
2. **인증서 비밀번호**: 환경 변수로만 관리, 코드에 하드코딩 금지
3. **SFTP 자격증명**: 암호화된 저장소 사용 권장
4. **로그 파일**: 민감 정보 마스킹 처리 필요
5. **스크린샷**: 에러 스크린샷에 민감 정보 노출 주의

---

## 라이센스

이 프로젝트는 내부 사용 목적의 RPA 솔루션입니다.

---

## 작성자 정보

- **작성자**: 김도영
- **프로젝트 버전**: 1.1.7
- **최종 수정**: 2026-10-14
