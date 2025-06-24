import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

class PM10Predictor:
    def __init__(self, model_path='models/pm10_model.pkl'):
        self.model_path = model_path
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.features = ['temperature', 'humidity', 'wind_speed']

    def train(self, x_train, y_train):
        """모델 학습"""
        self.model.fit(x_train, y_train)

    def predict(self, x):
        """예측 수행"""
        return self.model.predict(x)
    
    def evaluate(self, x_test, y_test):
        """모델 성능 평가"""
        predictions = self.predict(x_test)

        # mae 계산
        mae = mean_absolute_error(y_test, predictions)

        # rmse 계산
        rmse = np.sqrt(mean_squared_error(y_test, predictions))

        return {
            'mae' : mae,
            'rmse' : rmse
        }
    
    def save_model(self)