import os
import optuna
import yaml
import pandas as pd
from catboost import CatBoostRegressor, Pool
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt


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

    def prepare_data(self, train_data, test_data, model_type="catboost"):
        """Train/Test 데이터에서 Feature와 Target을 분리 (Categorical Features 제외)"""
        numerical_features = self.config.data_params["numerical_features"]
        features = numerical_features
        categorical_features = None
        if model_type == "catboost":
            categorical_features = self.config.data_params["categorical_features"]
            features = numerical_features + categorical_features
        target_column = self.config.data_params["target_column"]
        
        X_train = train_data[features]  # Feature만 선택
        y_train = train_data[target_column]  # Target (matching_score)
        X_test = test_data[features]
        y_test = test_data[target_column]

        return X_train, X_test, y_train, y_test, categorical_features

    def objective(self, trial):
        """Optuna 최적화 목표 함수"""
        train_data, test_data = self.load_data()
        X_train, X_test, y_train, y_test, categorical_features = self.prepare_data(train_data, test_data, model_type=self.model_type.lower())
        
        if self.model_type == "catboost":
            params = {
                "iterations": trial.suggest_int("iterations", 100, 1000),
                "depth": trial.suggest_int("depth", 4, 10),
                "learning_rate": trial.suggest_loguniform("learning_rate", 0.01, 0.3),
                "l2_leaf_reg": trial.suggest_loguniform("l2_leaf_reg", 1e-3, 10),
                "random_seed": 42,
                "verbose": 0,
                "od_type": "Iter",  # 조기 종료 옵션 추가
                "od_wait": 50,  # 50번 이상 개선되지 않으면 종료
                "task_type": "GPU"
            }
            train_pool = Pool(X_train, y_train, cat_features=categorical_features)
            model = CatBoostRegressor(**params)
            model.fit(train_pool, early_stopping_rounds=50)

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

        # 예측값 가져오기
        y_pred_scores = model.predict(X_test)

        # RMSE 계산
        rmse = sqrt(mean_squared_error(y_test, y_pred_scores))

        return rmse  # Optuna가 RMSE 값을 최소화하도록 설정

    def run(self):
        """Optuna 최적화 실행"""
        print(f"Optuna를 이용한 {self.model_type} 하이퍼파라미터 튜닝 시작...")
        study = optuna.create_study(direction="minimize")
        study.optimize(self.objective, n_trials=self.n_trials)

        print(f"✅ 최적의 하이퍼파라미터: {study.best_params}")
        self.save_best_params(study.best_params)

    def save_best_params(self, best_params):
        """config.yaml의 xgboost/catboost 부분만 업데이트"""
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