import data_collector

if __name__ == "__main__":
    collector = data_collector.DataCollector()
    df = collector.get_air_quality_data()
    print(df)