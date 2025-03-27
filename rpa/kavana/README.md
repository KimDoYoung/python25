# kavana

## 개요

- RPA관련 라이브러리 작성
- 그것을 이용해서 kfs-rpa-script 생성
- 최종적으로는 kfs-auto.exe, a.kas, .env  제공한다.

## make.sh

- make.sh로 compile
- 기능
    * venv 확인 및 활성화
    * pyinstaller 위치 확인 (venv 안에 있어야 함)
    * MODE=onedir 또는 MODE=onefile 선택 가능
    * onefile 모드 → --runtime-tmpdir 지정
    * onedir 모드 → kavana 폴더 전체 복사
    * 실행 파일 또는 실행 폴더를 $HOME/bin으로 복사
```shell
pyi-makespec --onefile --name kavana kavana.py
pyinstaller kavana.spec
```
```bash
./make.sh           # 기본: --onefile
./make.sh onefile   # 명시적: --onefile
./make.sh onedir    # 빠른 실행을 위한 --onedir 빌드
```


## mkdocs사용

```shell
mkdocs serve           # 브라우저로 확인
mkdocs build           # site/ 폴더 생성
mkdocs gh-deploy       # GitHub Pages로 배포 가능
```