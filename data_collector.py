import requests
import pandas as pd
from datetime import datetime
import config

class DataCollector:
  def __init__(self):
    self.airkorea_base_url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc"
    self.weather_base_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"

  def get_air_quality_data(self):
    air_quality_data = []
    
    try:
      url = f"{self.airkorea_base_url}/getCtprvnRltmMesureDnsty"
      params = {
        'serviceKey' : config.AIRKOREA_API_KEY,
        'returnType' : 'json',
        'numOfRows' : '100',
        'pageNo' : '1',
        'sidoName' : '경기',
        'ver' : '1.0'
      }

      res = requests.get(url, params=params)
      data = res.json()

      # 예외처리
      if 'response' in data and 'body' in data['response']:
        items = data['response']['body']['items']

        # #측정소 위치 확인
        # for item in items:
        #   print(item['stationName'])  

        # 수원시 측정소 매핑
        station_mapping = {
          '장안구' : ['정자동', '천천동'],
          '권선구' : ['호매실', '고색동'],
          '팔달구' : ['인계동', '신풍동', '경수대로(동수원)'],
          '영통구' : ['광교동', '영통동']
        }
     
        # 필요한 데이터만 추출
        for district, stations in station_mapping.items():
          district_items = [item for item in items if item['stationName'] in stations]
          
          for item in district_items:
            air_quality_data.append({
              'district' : district,
              'station' : item['stationName'],
              'timestamp' : item['dataTime'],
              'pm10' : float(item['pm10Value']) if item['pm10Value'] not in ['', None] else None,
              'pm25' : float(item['pm25Value']) if item['pm25Value'] not in ['', None] else None
            })

    except Exception as e:
      print("데이터 수집 실패")
      print("[ERROR]: ",e)

    df = pd.DataFrame(air_quality_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    grouped = df.groupby(['district', 'timestamp']).agg({
      'pm10' : 'mean',
      'pm25' : 'mean'
    }).reset_index()

    return grouped
