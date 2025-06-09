from data_collector import DataCollector
from datetime import datetime
import pandas as pd
import os

def create_directories():
    """make needed directories"""
    
    os.makedirs('data', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    os.makedirs('maps', exist_ok=True)

def save_to_csv(df, filename):
    """save merged_df to ./data/historical_data.csv"""
    
    file_path = f'data/{filename}'
    
    df.to_csv(
            file_path,
            mode='w', # write (덮어쓰기)
            header=True, # 헤더 항상 포함
            index=False,
            encoding='utf-8-sig'
        )
    print(f"[INFO] 데이터 {len(df)}건 저장됨")

def load_csv(filename):
    """CSV 파일 로드"""
    
    try:
        return pd.read_csv(f'data/{filename}')
    except FileNotFoundError as e:
        print(f"[ERROR] load_csv(): {e}")

def update_data():
    """collect data and update"""
    
    print(f'[{datetime.now()}] 데이터 수집 시작')
    
    collector = DataCollector()
    current_data = collector.collect_and_merge_data()
        
    # 소수점 2자리로 반올림
    float_cols = ['pm10','pm25','humidity','temperature','wind_speed']
    for col in float_cols:
        if col in current_data.columns:
            current_data[col] = current_data[col].round(2).astype(str).astype(float) # 부동소수점 제거
    
    # 기존 데이터와 병합
    historical_data = load_csv('historical_data.csv')
    if historical_data is not None:
        """
        csv에서 데이터 불러올 때 문자열로 가져오는데 그래서 str vs datetime으로 중복 비교를 하기 때문에 중복 아님으로 처리됨
        그래서 둘 다 datetime 타입으로 변환 후 중복 제거
        """
        historical_data['timestamp'] = pd.to_datetime(historical_data['timestamp'])
        current_data['timestamp'] = pd.to_datetime(current_data['timestamp']) 
        current_data = pd.concat([historical_data, current_data])
        current_data = current_data.drop_duplicates().reset_index(drop=True) # 중복 제거
    
    # 데이터 저장
    if not current_data.empty:
        save_to_csv(current_data, 'historical_data.csv')
    else:
        print('[WARNING] 수집된 데이터 없음')

    print(f'{datetime.now()} 데이터 수집 완료')
    return current_data

def main():
    """메인 실행 함수"""
    
    create_directories()
    data = update_data()
    

if __name__ == "__main__":
    main()
    