import os
import optuna
import yaml
from math import sqrt
import pandas as pd
from sklearn.metrics import mean_squared_error
from catboost import CatBoostRegressor, Pool
from xgboost import XGBRegressor


class OptunaOptimizer:
    def __init__(self, config, model_type="catboost", n_trials=5):
        self.config = config
        self.model_type = model_type.lower()
        self.n_trials = n_trials

    def load_data(self):
        """데이터 로드"""
        train_path = os.path.join(self.config.data_path, "train.csv")
        test_path = os.path.join(self.config.data_path, "test.csv")

        train_data = pd.read_csv(train_path)
        test_data = pd.read_csv(test_path)

        return train_data, test_data

    def prepare_data(self, train_data, test_data):
        """Feature 및 Target 분리"""
        features = self.config.data_params["numerical_features"]
        target_column = self.config.data_params["target_column"]

        X_train = train_data[features]
        y_train = train_data[target_column]
        X_test = test_data[features]
        y_test = test_data[target_column]

        return X_train, X_test, y_train, y_test

    def objective(self, trial):
        """Optuna 최적화 목표 함수"""
        train_data, test_data = self.load_data()
        X_train, X_test, y_train, y_test = self.prepare_data(train_data, test_data)

        if self.model_type == "catboost":
            params = {
                "iterations": trial.suggest_int("iterations", 100, 1000),
                "depth": trial.suggest_int("depth", 4, 10),
                "learning_rate": trial.suggest_loguniform("learning_rate", 0.01, 0.3),
                "l2_leaf_reg": trial.suggest_loguniform("l2_leaf_reg", 1e-3, 10),
                "random_seed": 42,
                "verbose": 0
            }
            model = CatBoostRegressor(**params)
            train_pool = Pool(X_train, y_train)
            model.fit(train_pool)

        elif self.model_type == "xgboost":
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
                "max_depth": trial.suggest_int("max_depth", 3, 10),
                "learning_rate": trial.suggest_loguniform("learning_rate", 0.01, 0.3),
                "subsample": trial.suggest_uniform("subsample", 0.5, 1.0),
                "colsample_bytree": trial.suggest_uniform("colsample_bytree", 0.5, 1.0),
                "reg_lambda": trial.suggest_loguniform("reg_lambda", 1e-3, 10),
                "random_state": 42
            }
            model = XGBRegressor(**params)
            model.fit(X_train, y_train)

        else:
            raise ValueError("지원되지 않는 모델입니다. 'catboost' 또는 'xgboost'를 선택하세요.")

        predictions = model.predict(X_test)
        rmse = sqrt(mean_squared_error(y_test, predictions))
        return rmse

    def run(self):
        """Optuna 최적화 실행"""
        print(f"Optuna를 이용한 {self.model_type} 하이퍼파라미터 튜닝 시작...")
        study = optuna.create_study(direction="minimize")
        study.optimize(self.objective, n_trials=self.n_trials)

        print(f"✅ 최적의 하이퍼파라미터: {study.best_params}")
        self.save_best_params(study.best_params)

    def save_best_params(self, best_params):
        f"""config.yaml의 xgboost/catboost 부분만 업데이트"""
        config_path = "config/config.yaml"  # 기존 config 파일 경로

        # 1️⃣ 기존 YAML 파일 로드
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config_data = yaml.safe_load(f)  # 기존 설정 불러오기
        else:
            config_data = {}  # 파일이 없으면 빈 딕셔너리 생성

        # 2️⃣ catboost_params 부분 업데이트
        if f"{self.model_type}_params" not in config_data:
            config_data["catboost_params"] = {}

        config_data[f"{self.model_type}_params"].update(best_params)

        # 3️⃣ 업데이트된 설정을 다시 저장
        with open(config_path, "w") as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)

        print(f"📢 {self.model_type}_params 업데이트 완료: {config_path}")