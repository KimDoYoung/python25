# kavana

## 개요

- RPA관련 라이브러리 작성
- 그것을 이용해서 kfs-rpa-script 생성
- 최종적으로는 kfs-auto.exe, a.kas, .env  제공한다.

## make.sh

- make.sh로 compile

```shell
pyi-makespec --onefile --name kavana kavana.py
pyinstaller kavana.spec
```

## RPA commands

- CAPTURE
- SLEEP
- WAIT
- CLICK
- MOVE
- RUN

