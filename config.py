from dotenv import load_dotenv
import os

# .env 불러오기
load_dotenv()

# API 키
AIRKOREA_API_KEY = os.getenv('AIRKOREA_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')