import psutil

# 현재 실행 중인 모든 프로세스 목록 출력
for proc in psutil.process_iter(attrs=['pid', 'name']):
    print(proc.info)

