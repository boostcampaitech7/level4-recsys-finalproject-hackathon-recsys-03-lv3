import os
import pandas as pd

from sqlalchemy import text

from api.db import SessionLocal
from src.utils import check_path


def load_data(data_path: str):
    """
    DB에서 데이터 로드 후 CSV 파일로 저장

    Args:
        data_path (str): 데이터 저장 경로
    """
    db = SessionLocal()

    try:
        sql_project = """
            SELECT  P.PROJECT_ID AS project_id,
                    TO_CHAR(P.PROJECT_CONTENT) AS project_content,
                    P.DURATION AS duration,
                    P.BUDGET AS budget,
                    P.PRIORITY AS priority,
                    P.COMPANY_ID AS company_id,
                    P.CATEGORY_ID AS category_id,
                    JSON_ARRAYAGG(PS.SKILL_ID) AS skill_id
            FROM    PROJECT P
            JOIN    PROJECT_SKILL PS ON P.PROJECT_ID = PS.PROJECT_ID
            WHERE   P.STATUS IN (1, 2)
            GROUP BY P.PROJECT_ID, TO_CHAR(P.PROJECT_CONTENT), P.DURATION, P.BUDGET, P.PRIORITY, P.COMPANY_ID, P.CATEGORY_ID
            """

        sql_freelancer = """
            SELECT  F.FREELANCER_ID AS freelancer_id,
                    F.WORK_EXP AS work_exp,
                    F.PRICE AS price,
                    JSON_ARRAYAGG(FS.SKILL_ID) AS skill_id,
                    JSON_ARRAYAGG(FC.CATEGORY_ID) AS category_id
            FROM    FREELANCER F
            JOIN    FREELANCER_SKILL FS ON F.FREELANCER_ID = FS.FREELANCER_ID
            JOIN    FREELANCER_CATEGORY FC ON F.FREELANCER_ID = FC.FREELANCER_ID
            GROUP BY F.FREELANCER_ID, F.WORK_EXP, F.PRICE
            """

        sql_inter = """
            SELECT  PROJECT_ID AS project_id,
                    FREELANCER_ID AS freelancer_id,
                    MATCHING_SCORE AS matching_score
            FROM (
                SELECT  PROJECT_ID,
                        FREELANCER_ID,
                        MATCHING_SCORE,
                        ROW_NUMBER() OVER (PARTITION BY PROJECT_ID ORDER BY MATCHING_SCORE DESC) AS RANKING
                FROM    PROJECT_RANKING
            )
            WHERE RANKING <= 10
            """

        project_df = pd.read_sql(text(sql_project), db.bind)
        freelancer_df = pd.read_sql(text(sql_freelancer), db.bind)
        inter_df = pd.read_sql(text(sql_inter), db.bind)

        check_path(data_path)
        project_df.to_csv(os.path.join(data_path, "project.csv"), index=False)
        freelancer_df.to_csv(os.path.join(data_path, "freelancer.csv"), index=False)
        inter_df.to_csv(os.path.join(data_path, "inter.csv"), index=False)

    except Exception as e:
        print(f"데이터 로드 중 오류 발생: {e}")

    finally:
        db.close()

def prepare_catboost_data(data_path: str):
    """
    CatBoost 모델용 데이터 준비 함수 (매칭 점수 예측).
    기존 프로젝트, 프리랜서, 매칭 데이터를 결합하여 학습 데이터를 생성.

    Args:
        data_path (str): 데이터 저장 경로
    """
    project_path = os.path.join(data_path, "project.csv")
    freelancer_path = os.path.join(data_path, "freelancer.csv")
    inter_path = os.path.join(data_path, "inter.csv")

    project_data = pd.read_csv(project_path)
    freelancer_data = pd.read_csv(freelancer_path)
    inter_data = pd.read_csv(inter_path)

    # 데이터 결합
    merged_data = pd.merge(inter_data, project_data, on="project_id", how="inner")
    merged_data = pd.merge(merged_data, freelancer_data, on="freelancer_id", how="inner")

    # Train/Test 분리
    train_data = merged_data.sample(frac=0.8, random_state=42)
    test_data = merged_data.drop(train_data.index)

    # 데이터 저장
    check_path(data_path)
    train_data.to_csv(os.path.join(data_path, "train.csv"), index=False)
    test_data.to_csv(os.path.join(data_path, "test.csv"), index=False)
