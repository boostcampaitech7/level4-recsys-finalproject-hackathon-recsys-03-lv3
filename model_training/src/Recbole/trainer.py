import os
import pandas as pd
import torch
import argparse
from typing import Tuple

from recbole.config import Config
from recbole.trainer import Trainer
from recbole.data.dataset import Dataset
from recbole.data.interaction import Interaction


def train(
    args: argparse.Namespace,
    config: Config,
    model_class: type,
    data_list: Tuple[Dataset, Dataset, Dataset]
):
    """
    모델을 학습 및 평가한 후, 선택적으로 추천 결과를 CSV로 저장

    Args:
        args (argparse.Namespace): CLI에서 받은 argparse 파싱 결과
        config (Config): RecBole 설정 객체. 데이터셋 경로, 필드 정보, 전처리 설정 등을 포함
        model_class (type): RecBole 모델 클래스
        data_list (Tuple[Dataset, Dataset, Dataset]): 학습(train), 검증(valid), 테스트(test) 데이터셋
    """

    tr_data, val_data, te_data = data_list

    model = model_class(config, tr_data.dataset).to(config["device"])
    trainer = Trainer(config, model)

    print("📍 train start ========================================")
    best_valid_score, best_valid_result = trainer.fit(train_data=tr_data, valid_data=val_data)
    print(f"🤟 best valid score & result: {best_valid_score}, {best_valid_result}")

    print("📍 evaluation start ===================================")
    test_result = trainer.evaluate(te_data)
    print(f"🤟 test_result: {test_result}")

    if args.csv:
        print("📍 prediction start ==================================")
        model.eval()

        dataset = te_data.dataset
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # GPU 사용 가능하면 활용
        config["device"] = device

        # inter_df에서 (user_id, item_id) 조합 불러오기
        inter_df = pd.read_csv(os.path.join(args.data_path, "inter.csv"))

        # RecBole 내부 index로 변환
        user_ids = torch.tensor(
            [dataset.token2id(dataset.uid_field, str(uid)) for uid in inter_df["project_id"].to_numpy()],
            device=device, dtype=torch.long
        )
        item_ids = torch.tensor(
            [dataset.token2id(dataset.iid_field, str(iid)) for iid in inter_df["freelancer_id"].to_numpy()],
            device=device, dtype=torch.long
        )

        # Interaction 객체 생성
        interaction = Interaction({
            config["USER_ID_FIELD"]: user_ids,
            config["ITEM_ID_FIELD"]: item_ids,
        }).to(device)

        # 매칭 점수 예측
        with torch.no_grad():
            scores = model.predict(interaction).cpu().numpy()

        # 결과 저장
        df = pd.DataFrame({
            'project_id': inter_df["project_id"],
            'freelancer_id': inter_df["freelancer_id"],
            'matching_score': scores
        })

        # CSV 저장
        output_path = os.path.join(args.output_path, f"{config.model}.csv")
        df.to_csv(output_path, index=False)
        print(f"✅ Matching results saved to {output_path}")
