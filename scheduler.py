import sys
import schedule
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import atexit
from datetime import datetime
from main import update_data

# logs 디렉토리 생성
os.makedirs("logs", exist_ok=True)

# 핸들러 생성: 자정마다 새 파일 생성, 백업 파일은 최대 7개
handler = TimedRotatingFileHandler(
    filename='logs/scheduler.log',
    when='midnight',
    interval=1,
    backupCount=7,
    encoding='utf-8'
)

# 로그 포맷 설정
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 루트 로거 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

lock_file = 'scheduler.lock'

# 다른 인스턴스가 이미 실행 중이라면 종료
if os.path.exists(lock_file):
    print("이미 실행중임")
    sys.exit
    
# 락 파일 생성
with open(lock_file, 'w') as f:
    f.write('running')
    
# 종료 시 락 파일 삭제
atexit.register(lambda: os.remove(lock_file))

# 로그 설정
logging.basicConfig(
    filename=f"logs/{datetime.now().strftime('%Y-%m-%d')}_scheduler.log",
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    encoding='utf-8'
)

def job():
        
    logging.info("데이터 수집 시작")
    try:
        update_data()
        logging.info("데이터 수집 완료")
    except Exception as e:
       logging.error(f"데이터 수집 중 에러 발생", exc_info=True) 

# 매시 55분마다 수집
schedule.every().hour.at(":55").do(job)

# 테스트용
# schedule.every(1).minutes.do(job)

logging.info(f"{time.ctime()} -  자동 스케쥴러 활성화")

while True:
    try:
        schedule.run_pending()
        time.sleep(60)
    except Exception as e:
        logging.critical("스케쥴러 루프에서 예기치 못한 에러 발생", exc_info=True)