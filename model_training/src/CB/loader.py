import os
import pandas as pd
from ast import literal_eval
from src.utils import check_path


def prepare_data(data_path: str, config):
    """
    CatBoost용 데이터셋 생성 (프로젝트와 프리랜서 데이터를 결합).
    
    Args:
        data_path (str): 데이터 저장 경로
        config: config.yaml 설정값
    """
    project_path = os.path.join(data_path, "project.csv")
    freelancer_path = os.path.join(data_path, "freelancer.csv")
    inter_path = os.path.join(data_path, "inter.csv")

    project_data = pd.read_csv(project_path)
    freelancer_data = pd.read_csv(freelancer_path)
    inter_data = pd.read_csv(inter_path)

    # 컬럼명 변경 (프리랜서와 프로젝트를 구분)
    project_data = project_data.rename(columns={
        "category_id": "project_category",
        "skill_id": "project_skills",
        "budget": "project_budget",
        "duration": "project_duration",
        "priority": "project_priority",
        "company_id": "project_company",
        "project_content": "project_description"
    })

    freelancer_data = freelancer_data.rename(columns={
        "category_id": "freelancer_category",
        "skill_id": "freelancer_skills",
        "price": "freelancer_price",
        "work_exp": "freelancer_experience"
    })
    
    # 🔹 스킬 리스트를 문자열에서 리스트로 변환
    project_data["project_skills"] = project_data["project_skills"].apply(lambda x: ",".join(map(str, literal_eval(x))))
    freelancer_data["freelancer_skills"] = freelancer_data["freelancer_skills"].apply(lambda x: ",".join(map(str, literal_eval(x))))

    # 데이터 결합 (매칭 점수를 포함)
    merged_data = pd.merge(inter_data, project_data, on="project_id", how="inner")
    merged_data = pd.merge(merged_data, freelancer_data, on="freelancer_id", how="inner")

    # 프로젝트 단위 Train/Test 분리
    unique_projects = merged_data["project_id"].unique()
    unique_projects.sort()  # 프로젝트 ID 정렬 (재현성을 위해)
    
    train_ratio = config.data_params["train_ratio"]
    num_train = int(len(unique_projects) * train_ratio)

    train_projects = unique_projects[:num_train]  # 앞부분 train_ratio 만큼 사용
    test_projects = unique_projects[num_train:]  # 나머지 test 사용

    train_data = merged_data[merged_data["project_id"].isin(train_projects)]
    test_data = merged_data[merged_data["project_id"].isin(test_projects)]

    # 저장
    check_path(data_path)
    train_data.to_csv(os.path.join(data_path, "train.csv"), index=False)
    test_data.to_csv(os.path.join(data_path, "test.csv"), index=False)
