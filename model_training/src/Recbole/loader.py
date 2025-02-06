import os
import pandas as pd

from typing import Tuple
from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from recbole.data.dataset import Dataset as RecBoleDataset

from src.utils import check_path


def get_data(config: Config) -> Tuple[RecBoleDataset, RecBoleDataset, RecBoleDataset]:
    """
    RecBole 형식에 맞게 data를 생성하고, train/valid/test로 나누는 메서드

    Args:
        config (Config): RecBole 설정 객체. 데이터셋 경로, 필드 정보, 전처리 설정 등을 포함

    Returns:
        Tuple[Dataset, Dataset, Dataset]: 학습 데이터, 검증 데이터, 테스트 데이터 반환
                                          (각 데이터는 RecBole의 Dataset 객체로, Interaction 형태의 데이터를 포함)
    """
    print("📍 spliting data ======================================")
    dataset = create_dataset(config)
    train_data, valid_data, test_data = data_preparation(config=config, dataset=dataset)
    return train_data, valid_data, test_data


def generate_data(data_path, config: Config):
    """
    data를 불러와 전처리한 후, Recbole의 .user, .item, .inter 데이터로 변환하는 함수

    Args:
        data_path (str): 데이터 저장 경로
        config (Config): RecBole 설정 객체. 데이터셋 경로, 필드 정보, 전처리 설정 등을 포함
    """
    print("📍 generating data ====================================")
    project_df = pd.read_csv(os.path.join(data_path, "project.csv"))
    freelancer_df = pd.read_csv(os.path.join(data_path, "freelancer.csv"))
    inter_df = pd.read_csv(os.path.join(data_path, "inter.csv"))

    rating_name = "rating:float"
    if config.model in ("FM", "FFM", "DeepFM"):
        rating_name = "label:float"

    # 컬럼명을 RecBole 표준 포맷으로 변경
    inter_df.rename(columns={"project_id": "user_id:token",
                             "freelancer_id": "item_id:token",
                             "matching_score": rating_name}, inplace=True)
    freelancer_df.rename(columns={"freelancer_id": "item_id:token",
                                  "work_exp": "work_exp:float",
                                  "price": "price:float",
                                  "category_id": "category:list"}, inplace=True)
    project_df.rename(columns={"project_id": "user_id:token",
                               "duration": "duration:float",
                               "budget": "budget:float",
                               "priority": "priority:token",
                               "company_id": "company_id:token",
                               "category_id": "category:list"}, inplace=True)

    # RecBole용 `.inter`, `.user`, `.item` 저장
    recbole_data_path, recbole_data_name = config.data_path, config.dataset
    check_path(recbole_data_path)
    project_df.to_csv(os.path.join(recbole_data_path, f"{recbole_data_name}.user"), index=False, sep="\t")
    freelancer_df.to_csv(os.path.join(recbole_data_path, f"{recbole_data_name}.item"), index=False, sep="\t")
    inter_df.to_csv(os.path.join(recbole_data_path, f"{recbole_data_name}.inter"), index=False, sep="\t")
