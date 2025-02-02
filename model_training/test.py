from src.dataset import prepare_catboost_data
from omegaconf import OmegaConf

# config.yaml 로드
config = OmegaConf.load("config/config.yaml")

# 데이터 생성 실행
prepare_catboost_data("datasets/", config)

print("데이터 준비 완료: train.csv & test.csv 생성됨.")
