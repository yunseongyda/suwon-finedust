from dotenv import load_dotenv
import os

# .env 불러오기
load_dotenv()

# API 키
AIRKOREA_API_KEY = os.getenv('AIRKOREA_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

# 수원시 구별 중심 좌표 (위도, 경도)
DISTRICT_COORDINATES = {
  '장안구': (37.3099, 127.0129),
  '권선구': (37.2575, 126.9726),
  '팔달구': (37.2843, 127.0305),
  '영통구': (37.2652, 127.0714)
}