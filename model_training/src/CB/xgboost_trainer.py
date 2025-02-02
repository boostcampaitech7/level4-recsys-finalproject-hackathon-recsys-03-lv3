import os
import pickle
import pandas as pd
import numpy as np
from datetime import datetime  # 🔹 타임스탬프 추가
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from math import sqrt

class XGBoostTrainer:
    def __init__(self, config):
        self.config = config
        self.model = XGBRegressor(**config.xgboost_params)

    def load_data(self):
        """저장된 Train/Test 데이터를 로드"""
        train_path = os.path.join(self.config.data_path, "train.csv")
        test_path = os.path.join(self.config.data_path, "test.csv")

        train_data = pd.read_csv(train_path)
        test_data = pd.read_csv(test_path)

        return train_data, test_data

    def prepare_data(self, train_data, test_data):
        """Train/Test 데이터에서 Feature와 Target을 분리 (Categorical Features 제외)"""
        features = self.config.data_params["numerical_features"]
        target_column = self.config.data_params["target_column"]

        X_train = np.array(train_data[features])  # Feature만 선택
        y_train = np.array(train_data[target_column])  # Target (matching_score)
        X_test = np.array(test_data[features])
        y_test = np.array(test_data[target_column])

        return X_train, X_test, y_train, y_test

    def run(self):
        """XGBoost 모델 학습 및 평가"""
        train_data, test_data = self.load_data()
        X_train, X_test, y_train, y_test = self.prepare_data(train_data, test_data)

        print("🔹 XGBoost 모델 학습 시작...")
        self.model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=100)

        # 예측 및 평가
        predictions = self.model.predict(X_test)

        rmse = sqrt(mean_squared_error(y_test, predictions))
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        print(f"✅ 테스트 RMSE: {rmse:.4f}")
        print(f"✅ 테스트 MAE: {mae:.4f}")
        print(f"✅ 테스트 R^2: {r2:.4f}")

        # 🔹 저장 파일명 동적으로 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 현재 시간
        model_path_pkl = os.path.join(self.config.output_path, f"xgboost_model_{timestamp}.pkl")

        # 저장 디렉토리 생성
        os.makedirs(self.config.output_path, exist_ok=True)

        # Pickle(.pkl) 형식으로 저장
        with open(model_path_pkl, "wb") as f:
            pickle.dump(self.model, f)

        print(f"📢 모델이 저장되었습니다: {model_path_pkl}")
