import os
import logging
from datetime import datetime

# 로그 설정
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/scheduler.log",
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    encoding='utf-8'
)

# 락 파일 삭제
lock_file = "scheduler.lock"

if os.path.exists(lock_file):
    os.remove(lock_file)
    logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 수동 종료: 락 파일 제거됨")
    print("Successfully stopped scheduler")
else:
    logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 수동 종료 시도: 락 파일 없음")
    print("There is no lock file to terminate")