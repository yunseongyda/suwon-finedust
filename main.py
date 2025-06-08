from data_collector import DataCollector
from datetime import datetime
import pandas as pd
import os

def create_directories():
    """필요한 디렉토리(폴더) 생성 / mkdir"""
    


if __name__ == "__main__":
    collector = DataCollector()
    df = collector.collect_and_merge_data()