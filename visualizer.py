import folium
import pandas as pd
from config import GRADE_COLORS, PM10_GRADE, PM25_GRADE, DISTRICT_COORDINATES

class MapVisualizer():
    def __init__(self, csv_path='data/historical_data.csv'):
        self.csv_path = csv_path
        self.center = [37.2751, 127.0276] # 수원시 중심좌표
        
    def get_latest_data(self):
        """최근 데이터 가져오기"""
        df = pd.read_csv(self.csv_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        latest_time = df['timestamp'].max()    # 가장 최근 값 가져오기
        latest_df = df[df['timestamp'] == latest_time]
        
        return latest_df
    
    def value_to_grade(self, value, grade_dict):
        """미세먼지 값을 등급으로 변환"""
        for grade, (low, high) in grade_dict.items():
            if low <= value <= high:
                return grade
        return "unknown"
    
    def pm10_to_color(self, pm10):
        """pm10 값을 색상으로 반환"""
        for grade, (low, high) in PM10_GRADE.items():
            if low <= pm10 <= high:
                return GRADE_COLORS[grade]
        return "gray"
    
    def create_base_map(self):
        """기본 지도 생성"""
        return folium.Map(location=self.center,
                        zoom_start=12,
                        tiles='cartodbpositron')

    def draw_map(self, m, save_path='maps/latest_map.html'):
        """지도 그리기"""
        latest_df = self.get_latest_data()
        
        for _, row in latest_df.iterrows():
            dist = row['district']
            pm10 = row['pm10']
            pm25 = row['pm25']
            lat, lon = DISTRICT_COORDINATES[dist] # 해당 구의 위도, 경도 가져오기
            
            pm10_grade = self.value_to_grade(pm10, PM10_GRADE)
            pm25_grade = self.value_to_grade(pm25, PM25_GRADE)
            
            popup_text = f'{dist}<br>PM10: {pm10} <b>({pm10_grade})</b><br>PM2.5: {pm25} <b>({pm25_grade})</b>'
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=50,
                color=self.pm10_to_color(pm10),
                fill=True,
                fill_color=self.pm10_to_color(pm10),
                fill_opacity=0.4,
                popup=popup_text
            ).add_to(m)
            
        m.save(save_path)
        print("[INFO] 지도 저장 완료")


    def create_map(self):
        """전체 지도 생성"""
        # 기본 지도 생성
        map_obj = self.create_base_map()

        self.draw_map(map_obj)