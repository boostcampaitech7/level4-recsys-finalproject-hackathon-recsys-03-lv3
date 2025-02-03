import os
import random
import numpy as np
import pandas as pd
import torch


def set_seed(seed):
    """
    재현성을 위한 랜덤 시드를 설정하는 메서드
    다양한 라이브러리의 랜덤 시드를 설정 (Python의 random 모듈, Numpy, PyTorch(CPU 및 GPU))

    Args:
        seed (int): 랜덤 숫자 생성을 위한 시드 값
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True


def check_path(path: str) -> None:
    """
    디렉토리가 존재하는지 확인하고, 존재하지 않으면 생성하는 메서드

    Args:
        path (str): 확인하고 생성할 경로
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"{path} created")


def recall_at_k(y_true, y_pred, k=10):
    """
    Recall@K 계산 함수

    Args:
        y_true (dict): 실제 매칭된 프리랜서 목록 (key=project_id, value=set(freelancer_ids))
        y_pred (dict): 모델이 예측한 프리랜서 목록 (key=project_id, value=list(freelancer_ids))
        k (int): Recall@K의 K 값 (기본 10)

    Returns:
        float: Recall@K 평균 값
    """
    recalls = []

    for project_id in y_true.keys():
        true_freelancers = set(y_true[project_id])  # 실제 매칭된 프리랜서
        predicted_freelancers = set(y_pred.get(project_id, [])[:k])  # 모델이 추천한 상위 K명

        if len(true_freelancers) == 0:
            continue  # 매칭이 없는 프로젝트는 제외

        recall = len(true_freelancers & predicted_freelancers) / len(true_freelancers)
        recalls.append(recall)
    return np.mean(recalls) if recalls else 0.0  # 평균 Recall@K 반환


def load_true_matches(inter_path):
    """
    `inter.csv`에서 실제 매칭된 상위 10개 프리랜서 리스트 로드

    Args:
        inter_path (str): inter.csv 파일 경로

    Returns:
        dict: {project_id: set(freelancer_ids)}
    """
    inter_data = pd.read_csv(inter_path)

    # 프로젝트별로 상위 10개 매칭된 프리랜서만 선택
    y_true = (
        inter_data.sort_values(["project_id", "matching_score"], ascending=[True, False])
        .groupby("project_id")["freelancer_id"]
        .apply(lambda x: set(x.head(10)))  # 상위 10개만 선택
        .to_dict()
    )

    return y_true