import schedule
import time
from main import update_data

def job():
    print("[SCHEDULED] 미세먼지 데이터 수집 시작")
    update_data()
    print("[SCHEDULED] 수집 완료")

# 매시 20분마다 수집
schedule.every().hour.at(":20").do(job)

print("[INFO] 자동 스케쥴러 활성화")

while True:
    schedule.run_pending()
    time.sleep(60)