import os
import pickle
import pandas as pd
import numpy as np  # 🔹 NumPy 추가
from datetime import datetime  # 🔹 타임스탬프 추가
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from math import sqrt

class LogisticTrainer:
    def __init__(self, config):
        self.config = config
        self.model = LinearRegression()

    def load_data(self):
        """저장된 Train/Test 데이터를 로드"""
        train_path = os.path.join(self.config.data_path, "train.csv")
        test_path = os.path.join(self.config.data_path, "test.csv")

        train_data = pd.read_csv(train_path)
        test_data = pd.read_csv(test_path)

        return train_data, test_data

    def prepare_data(self, train_data, test_data):
        """Train/Test 데이터에서 Feature와 Target을 분리"""
        features = self.config.data_params["numerical_features"]
        target_column = self.config.data_params["target_column"]

        X_train = train_data[features]
        y_train = train_data[target_column]
        X_test = test_data[features]
        y_test = test_data[target_column]

        return X_train, X_test, y_train, y_test

    def run(self):
        """Linear Regression 모델 학습 및 평가"""
        train_data, test_data = self.load_data()
        X_train, X_test, y_train, y_test = self.prepare_data(train_data, test_data)

        # 🔹 매칭 점수를 0~1 범위로 변환
        y_prob = y_train / 100.0  # 매칭 점수 -> 확률값
        epsilon = 1e-6  # 로그 변환 안정성을 위한 작은 값 추가

        # 🔹 로짓 변환 적용
        y_logit = np.log(y_prob / (1 - y_prob + epsilon))

        # 모델 학습
        self.model.fit(X_train, y_logit)

        # 예측값 생성 (로짓 값)
        logit_predictions = self.model.predict(X_test)

        # 🔹 로짓 예측값을 확률(0~1)로 변환
        prob_predictions = 1 / (1 + np.exp(-logit_predictions))

        # 🔹 확률값을 다시 매칭 점수(0~100)로 변환
        predictions = prob_predictions * 100

        # 평가
        rmse = sqrt(mean_squared_error(y_test, predictions))
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        print(f"✅ 테스트 RMSE: {rmse:.4f}")
        print(f"✅ 테스트 MAE: {mae:.4f}")
        print(f"✅ 테스트 R^2: {r2:.4f}")

        # 🔹 저장 파일명 동적으로 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path_pkl = os.path.join(self.config.output_path, f"logistic_regression_model_{timestamp}.pkl")

        # 저장 디렉토리 생성
        os.makedirs(self.config.output_path, exist_ok=True)

        # Pickle(.pkl) 형식으로 저장
        with open(model_path_pkl, "wb") as f:
            pickle.dump(self.model, f)

        print(f"📢 Logistic Regression 모델이 저장되었습니다: {model_path_pkl}")
