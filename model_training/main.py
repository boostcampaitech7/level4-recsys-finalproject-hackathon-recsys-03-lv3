import argparse
import importlib
import logging
import warnings

from omegaconf import OmegaConf
from recbole.config import Config

from src.dataset import load_data
from src.utils import set_seed
from src.Recbole.loader import generate_data, get_data
from src.Recbole.trainer import train
from src.CB.catboost_trainer import CatBoostTrainer
from src.CB.xgboost_trainer import XGBoostTrainer
from src.CB.logistic_trainer import LogisticTrainer
from src.CB.loader import prepare_data
from src.CB.optuna_optimizer import OptunaOptimizer

logging.basicConfig(level=logging.INFO)
warnings.filterwarnings("ignore", category=FutureWarning)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    arg = parser.add_argument

    arg(
        "--config",
        "-c",
        help="Configuration 파일을 설정합니다.",
        default="config/config.yaml"
    )
    arg(
        "--data",
        "-d",
        help="DB 데이터 로드 여부를 선택합니다. (DB 데이터 갱신 시 사용)",
        default=False
    )
    arg(
        "--type",
        "-t",
        type=str,
        choices=["g", "s", "c"],
        help="model의 종류를 설정합니다. g:general, s:sequential, c:context-aware)",
        default=None
    )
    arg(
        "--model",
        "-m",
        type=str,
        help="추천 모델의 이름을 설정합니다. (참고: https://recbole.io/model_list.html)"
    )
    arg(
        "--optuna",
        "-o",
        help="트리 모델 사용 시, optuna를 이용하여 최적화를 먼저 수행할지 결정합니다. False 선택 시 저장된 하이퍼파라미터로 모델을 학습합니다.",
        default=False
    )

    args = parser.parse_args()

    config_args = OmegaConf.create(vars(args))
    config_yaml = OmegaConf.load(args.config)

    # 기본값을 명시적으로 설정하여 KeyError 방지
    if "type" not in config_yaml:
        config_yaml.type = None

    # args에 있는 값이 config_yaml에 있는 값보다 우선함. (단, None이 아닌 값일 경우)
    for key in config_args.keys():
        if config_args[key] is not None:
            config_yaml[key] = config_args[key]

    args = config_yaml

    set_seed(args.seed)

    if args.data:
        load_data(data_path=args.data_path)

    # Recbole 실행
    if args.type:
        model_type = {"g": "general_recommender", "s": "sequential_recommender", "c": "context_aware_recommender"}
        recbole_model = importlib.import_module("recbole.model." + model_type.get(args.type))
        model_class = getattr(recbole_model, args.model)

        # 1. Recbole Config 세팅
        config_path = "config/"
        config = Config(model=args.model, config_file_list=[config_path + "Recbole.yaml", config_path + args.model + ".yaml"])

        # 2. Recbole 데이터 생성 (/datasets/모델별 폴더에 저장)
        generate_data(data_path=args.data_path, config=config)

        # 3. Data Split
        tr_data, val_data, te_data = get_data(config)

        # 4. Train
        train(config=config, model_class=model_class, data_list=[tr_data, val_data, te_data])

    # 직접 구현한 모델
    else:
        config = OmegaConf.load("config/config.yaml")

        # 데이터 생성
        print("======== 데이터 생성 시작 ========")
        prepare_data("datasets/", config)
        print("======== 데이터 생성 완료 ========")

        # Optuna
        if args.optuna:
            print(f"======== Optuna 최적화 시작: {args.model} ========")
            optimizer = OptunaOptimizer(args, model_type=args.model.lower(), n_trials=50)
            optimizer.run()

        # CatBoost
        elif args.model.lower() == "catboost":
            print("======== CatBoost 모델 실행 시작 ========")
            catboost_trainer = CatBoostTrainer(args)
            catboost_trainer.run()

        # XGBoost
        elif args.model.lower() == "xgboost":
            print("======== XGBoost 모델 실행 시작 ========")
            xgboost_trainer = XGBoostTrainer(args)
            xgboost_trainer.run()

        # Logistic
        elif args.model.lower() == "logistic":
            print("======== Logistic Regression 모델 실행 시작 ========")
            logistic_trainer = LogisticTrainer(args)
            logistic_trainer.run()

        else:
            print("예외")
