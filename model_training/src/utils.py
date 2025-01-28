import os
import random
import numpy as np
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
