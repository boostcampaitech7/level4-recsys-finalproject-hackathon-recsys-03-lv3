import os
import pickle
from math import sqrt

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from src.utils import recall_at_k, ndcg_at_k


class LogisticTrainer:
    def __init__(self, config):
        self.config = config
        self.model = Lasso()

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

        y_prob = y_train / 100.0
        epsilon = 1e-6

        y_logit = np.log(y_prob / (1 - y_prob + epsilon))

        self.model.fit(X_train, y_logit)

        logit_predictions = self.model.predict(X_test)

        prob_predictions = 1 / (1 + np.exp(-logit_predictions))

        predictions = prob_predictions * 100

        rmse = sqrt(mean_squared_error(y_test, predictions))
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        print(f"🔍 Test RMSE: {rmse:.4f}")
        print(f"🔍 Test MAE: {mae:.4f}")
        print(f"🔍 Test R^2: {r2:.4f}")

        # 모델이 예측한 상위 10명 프리랜서 정리
        test_data["pred_score"] = predictions
        y_pred = (
            test_data.sort_values(["project_id", "pred_score"], ascending=[True, False])
            .groupby("project_id")["freelancer_id"]
            .apply(lambda x: list(x[:10]))
            .to_dict()
        )

        # 실제 매칭된 프리랜서 데이터 로드
        y_true = (
            test_data.sort_values(["project_id", "matching_score"], ascending=[True, False])
            .groupby("project_id")["freelancer_id"]
            .apply(lambda x: list(x[:10]))
            .to_dict()
        )

        # 평가
        recall_10 = recall_at_k(y_true, y_pred, k=10)
        print(f"🔍 Test Recall@10: {recall_10:.4f}")
        recall_5 = recall_at_k(y_true, y_pred, k=5)
        print(f"🔍 Test Recall@5: {recall_5:.4f}")
        ndcg_5 = ndcg_at_k(y_true, y_pred, k=5)
        print(f"🔍 Test NDCG@5: {ndcg_5:.4f}")

        # 학습된 모델 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path_pkl = os.path.join(self.config.output_path, f"logistic_regression_model_{timestamp}.pkl")

        os.makedirs(self.config.output_path, exist_ok=True)

        # Pickle(.pkl) 형식으로 저장
        with open(model_path_pkl, "wb") as f:
            pickle.dump(self.model, f)

        print(f"✔️ Logistic Regression 모델이 저장되었습니다: {model_path_pkl}")
