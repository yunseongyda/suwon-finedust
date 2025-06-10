import requests
import pandas as pd
from datetime import datetime, timedelta
import config

def latlon_to_xy(lat, lon):
    """위경도를 기상청 격자 좌표(nx, ny)로 변환"""
    import math

    RE = 6371.00877
    GRID = 5.0
    SLAT1 = 30.0
    SLAT2 = 60.0
    OLON = 126.0
    OLAT = 38.0
    XO = 43
    YO = 136
    DEGRAD = math.pi / 180.0

    re = RE / GRID
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)

    ra = math.tan(math.pi * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / math.pow(ra, sn)
    theta = lon * DEGRAD - olon
    if theta > math.pi: theta -= 2.0 * math.pi
    if theta < -math.pi: theta += 2.0 * math.pi
    theta *= sn

    x = ra * math.sin(theta) + XO
    y = ro - ra * math.cos(theta) + YO
    return int(x + 1.5), int(y + 1.5)


class DataCollector:
    def __init__(self):
        self.airkorea_base_url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc"
        self.weather_base_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"

    def get_air_quality_data(self):
        """airkorea에서 미세먼지 데이터 받아오기기"""
        air_quality_data = []
        INVALID_VALUES = ['', None, '-', '통신장애애']

        try:
            url = f"{self.airkorea_base_url}/getCtprvnRltmMesureDnsty"
            params = {
                'serviceKey': config.AIRKOREA_API_KEY,
                'returnType': 'json',
                'numOfRows': '100',
                'pageNo': '1',
                'sidoName': '경기',
                'ver': '1.0'
            }

            res = requests.get(url, params=params)
            if res.status_code != 200:
                print(f"[ERROR] 요청 실패: {res.status_code}")
                return pd.DataFrame() # 빈 DF 반환
            
            try:
                data = res.json()
            except Exception as e:
                print(f"[ERROR] JSON 디코딩 실패: {e}")
                return pd.DataFrame()

            if 'response' in data and 'body' in data['response']:
                items = data['response']['body']['items']

                station_mapping = {
                    '장안구': ['정자동', '천천동'],
                    '권선구': ['호매실', '고색동'],
                    '팔달구': ['인계동', '신풍동', '경수대로(동수원)'],
                    '영통구': ['광교동', '영통동']
                }

                # print(items)

                for district, stations in station_mapping.items():
                    district_items = [item for item in items if item['stationName'] in stations]

                    for item in district_items:
                        air_quality_data.append({
                            'district': district,
                            'station': item['stationName'],
                            'timestamp': item['dataTime'],
                            'pm10': float(item['pm10Value']) if item['pm10Value'] not in INVALID_VALUES else None,
                            'pm25': float(item['pm25Value']) if item['pm25Value'] not in INVALID_VALUES else None
                        })
                    if not air_quality_data:
                        print("[WARNING] 에어코리아 데이터 없음음")

        except Exception as e:
            print(f"[ERROR] 데이터 수집 실패: {e}")

        df = pd.DataFrame(air_quality_data)
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.floor('H')

        grouped = df.groupby(['district', 'timestamp']).agg({
            'pm10': 'mean',
            'pm25': 'mean'
        }).reset_index()

        print("\n[DEBUG] Final Air DataFrame: ")
        print(grouped)

        return grouped

    def get_weather_data(self, air_timestamp=None):
        """기상청 단기예보 API를 통해 날씨 데이터 수집"""
        weather_data = []
        now = datetime.now()

        if air_timestamp and (now - air_timestamp) > timedelta(minutes=30):
            print('[INFO] 기상청 시간 보정: {now} -> {air_timestamp}')
            now = air_timestamp

        base_date = now.strftime('%Y%m%d')
        minute = now.minute
        base_minute = (minute // 10) * 10
        base_time = now.replace(minute=base_minute, second=0, microsecond=0).strftime('%H%M')

        for dist, (lat, lon) in config.DISTRICT_COORDINATES.items():
            try:
                nx, ny = latlon_to_xy(lat, lon)

                url = f"{self.weather_base_url}/getUltraSrtNcst"
                params = {
                    'serviceKey': config.WEATHER_API_KEY,
                    'numOfRows': '100',
                    'pageNo': '1',
                    'dataType': 'JSON',
                    'base_date': base_date,
                    'base_time': base_time,
                    'nx': nx,
                    'ny': ny
                }

                res = requests.get(url, params=params)
                data = res.json()

                if 'response' in data and 'body' in data['response']:
                    items = data['response']['body']['items']['item']
                    info = {'district': dist, 'timestamp': now.strftime('%Y-%m-%d %H:%M')}

                    for item in items:
                        if item['category'] == 'T1H':
                            info['temperature'] = float(item['obsrValue'])
                        elif item['category'] == 'REH':
                            info['humidity'] = float(item['obsrValue'])
                        elif item['category'] == 'WSD':
                            info['wind_speed'] = float(item['obsrValue'])

                    weather_data.append(info)

            except Exception as e:
                print(f"[ERROR] {dist} 데이터 수집 실패: {e}")

        df = pd.DataFrame(weather_data)
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.floor('H')
        print("\n[DEBUG] Final weather DataFrame: ")
        print(df)

        return df

    def collect_and_merge_data(self):
        """현재 시점의 미세먼지 + 날씨 데이터를 수집하고 병합"""

        print('[INFO] 미세먼지 데이터 수집중...')
        air_df = self.get_air_quality_data()
        air_timestamp = air_df['timestamp'].max()

        print('[INFO] 날씨 데이터 수집중...')
        weather_df = self.get_weather_data(air_timestamp=air_timestamp)

        print('[INFO] 두 데이터 병합중...')
        merged_df = pd.merge(
            air_df,
            weather_df,
            on=['district', 'timestamp'],
            how='inner'
        )

        print('[INFO] 병합된 데이터: ')
        print(merged_df)

        return merged_df
