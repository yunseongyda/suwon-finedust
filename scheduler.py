import sys
import schedule
import time
import logging
import os
import atexit
from main import update_data

os.makedirs("logs", exist_ok=True)

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
    filename='logs/scheduler.log',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    encoding='utf-8'
)

def job():
        
    logging.info("미세먼지 데이터 수집 시작")
    try:
        update_data()
        logging.info("미세먼지 데이터 수집 완료")
    except Exception as e:
       logging.error(f"미세먼지 데이터 수집 중 에러 발생", exc_info=True) 

# 매시 20분마다 수집
schedule.every().hour.at(":20").do(job)

# 테스트용
# schedule.every(1).minutes.do(job)

logging.info(f"{time.ctime()} -  자동 스케쥴러 활성화")

while True:
    schedule.run_pending()
    time.sleep(60)