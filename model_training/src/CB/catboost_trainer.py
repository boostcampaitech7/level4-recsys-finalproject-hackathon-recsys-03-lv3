import os
import pandas as pd
from catboost import CatBoostRegressor, Pool
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from math import sqrt

class CatBoostTrainer:
    def __init__(self, config):
        self.config = config
        self.model = CatBoostRegressor(**config.catboost_params)

    def load_data(self):
        """프로젝트 및 프리랜서 데이터를 결합하여 데이터셋 생성"""
        project_path = os.path.join(self.config.data_path, "project.csv")
        freelancer_path = os.path.join(self.config.data_path, "freelancer.csv")
        inter_path = os.path.join(self.config.data_path, "inter.csv")

        project_data = pd.read_csv(project_path)
        freelancer_data = pd.read_csv(freelancer_path)
        inter_data = pd.read_csv(inter_path)

        # 데이터 결합 (프로젝트와 프리랜서 간 매칭 데이터)
        merged_data = pd.merge(inter_data, project_data, on="project_id", how="inner")
        merged_data = pd.merge(merged_data, freelancer_data, on="freelancer_id", how="inner")

        return merged_data

    def prepare_data(self, data):
        """CatBoost 모델용 데이터 준비"""
        features = [
            "budget", "skills_project", "category_project",  # 프로젝트 Feature
            "price", "work_exp", "category_freelancer", "skills_freelancer", "skill_temperature"  # 프리랜서 Feature
        ]

        categorical_features = [
            "skills_project", "category_project", "category_freelancer", "skills_freelancer"
        ]

        X = data[features]
        y = data["matching_score"]  # 매칭 점수

        return X, y, categorical_features

    def run(self):
        """CatBoost 모델 학습 및 평가"""
        data = self.load_data()
        X, y, categorical_features = self.prepare_data(data)

        # Train/Test Split
        train_size = int(len(data) * 0.8)
        X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
        y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]

        # CatBoost 데이터 Pool 생성
        train_pool = Pool(X_train, y_train, cat_features=categorical_features)
        test_pool = Pool(X_test, y_test, cat_features=categorical_features)

        # 모델 학습
        self.model.fit(train_pool, eval_set=test_pool, verbose=True)

        # 예측 및 평가
        predictions = self.model.predict(X_test)

        rmse = sqrt(mean_squared_error(y_test, predictions))
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        print(f"테스트 RMSE: {rmse:.4f}")
        print(f"테스트 MAE: {mae:.4f}")
        print(f"테스트 R^2: {r2:.4f}")

        # 모델 저장
        model_path = os.path.join(self.config.output_path, "catboost_model.cbm")
        self.model.save_model(model_path)
        print(f"모델이 저장되었습니다: {model_path}")
