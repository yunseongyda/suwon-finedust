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

# 미세먼지 등급 기준
PM10_GRADE = {
    '좋음': (0, 30),
    '보통': (31, 80),
    '나쁨': (81, 150),
    '매우나쁨': (151, 999)
}

# 초미세먼지 등급 기준
PM25_GRADE = {
    '좋음' : (0,15),
    '보통' : (16,50),
    '나쁨' : (51,100),
    '매우나쁨' : (100,999)
}

# 미세먼지 등급별 색상
GRADE_COLORS = {
    '좋음': '#32CD32',     # 초록
    '보통': '#FFD700',     # 노랑
    '나쁨': '#FF8C00',     # 주황
    '매우나쁨': '#FF0000'  # 빨강
}