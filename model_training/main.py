import argparse
import importlib
import logging
import warnings

from omegaconf import OmegaConf
from recbole.config import Config
from src.CB.catboost_trainer import CatBoostTrainer

from src.dataset import load_data
from src.utils import set_seed
from src.Recbole.loader import generate_data, get_data
from src.Recbole.trainer import train

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

    args = parser.parse_args()

    config_args = OmegaConf.create(vars(args))
    config_yaml = OmegaConf.load(args.config)

    # args에 있는 값이 config_yaml에 있는 값보다 우선함. (단, None이 아닌 값일 경우)
    for key in config_args.keys():
        if config_args[key] is not None:
            config_yaml[key] = config_args[key]

    args = config_yaml

    set_seed(args.seed)

    if args.data:
        load_data(data_path=args.data_path)

    # Recbole
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
        if args.model.lower() == "catboost":
            print("CatBoost 모델 실행 시작")
            catboost_trainer = CatBoostTrainer(args)
            catboost_trainer.run()
        else:
            print("예외처리")
