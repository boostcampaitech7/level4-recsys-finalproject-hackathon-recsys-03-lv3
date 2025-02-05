import json
import os

import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from sqlalchemy import text
from api.db import SessionLocal
from src.utils import check_path
from src.preprocessing import Preprocessing

from typing import Optional, Union


def load_data(data_path: str):
    """
    DB에서 데이터 로드 후 CSV 파일로 저장

    Args:
        data_path (str): 데이터 저장 경로
    """
    db = SessionLocal()

    try:
        sql_project_info = """
            SELECT  P.PROJECT_ID AS project_id,
                    P.DURATION AS duration,
                    ROUND(P.BUDGET / P.DURATION, 0) AS budget,
                    P.PRIORITY AS priority,
                    P.COMPANY_ID AS company_id,
                    (SELECT JSON_ARRAYAGG(PC.CATEGORY_ID)
                     FROM PROJECT PC
                     WHERE PC.PROJECT_ID = P.PROJECT_ID) AS category_id,
                    (SELECT JSON_ARRAYAGG(PS.SKILL_ID)
                     FROM PROJECT_SKILL PS
                     WHERE PS.PROJECT_ID = P.PROJECT_ID) AS skill_id
            FROM    PROJECT P
            JOIN    CATEGORY C ON P.CATEGORY_ID = C.CATEGORY_ID
            WHERE   P.STATUS IN (1, 2)
            """

        sql_project_content = """
            SELECT PROJECT_ID AS project_id,
                   DBMS_LOB.SUBSTR(PROJECT_CONTENT, 32767, 1) AS project_content
            FROM PROJECT
            WHERE STATUS IN (1, 2)
            """

        sql_freelancer = """
            SELECT  F.FREELANCER_ID AS freelancer_id,
                    F.WORK_EXP AS work_exp,
                    ROUND(F.PRICE / 365, 0) AS price,
                    (SELECT JSON_ARRAYAGG(FS.SKILL_ID) AS SKILL_ID
                     FROM FREELANCER_SKILL FS
                     WHERE FS.FREELANCER_ID = F.FREELANCER_ID) AS skill_id,
                    (SELECT JSON_ARRAYAGG(FS.SKILL_SCORE) AS SKILL_TEMP
                     FROM FREELANCER_SKILL FS
                     WHERE FS.FREELANCER_ID = F.FREELANCER_ID) AS skill_temp,
                    (SELECT JSON_ARRAYAGG(FC.CATEGORY_ID)
                     FROM FREELANCER_CATEGORY FC
                     WHERE FC.FREELANCER_ID = F.FREELANCER_ID) AS category_id
            FROM    FREELANCER F
            """

        sql_inter = """
            SELECT  PROJECT_ID AS project_id,
                    FREELANCER_ID AS freelancer_id,
                    MATCHING_SCORE AS matching_score
            FROM (
                SELECT  PROJECT_ID,
                        FREELANCER_ID,
                        MATCHING_SCORE / 100 AS MATCHING_SCORE,
                        ROW_NUMBER() OVER (PARTITION BY PROJECT_ID ORDER BY MATCHING_SCORE DESC) AS RANKING
                FROM    PROJECT_RANKING
            )
            ORDER BY PROJECT_ID, RANKING
            """

        sql_inter_implicit = """
            SELECT  PROJECT_ID AS project_id,
                    FREELANCER_ID AS freelancer_id,
                    (CASE WHEN RANKING <= 10 THEN 1
                          ELSE 0
                    END) AS matching_score
            FROM (
                SELECT  PROJECT_ID,
                        FREELANCER_ID,
                        ROW_NUMBER() OVER (PARTITION BY PROJECT_ID ORDER BY MATCHING_SCORE DESC) AS RANKING
                FROM    PROJECT_RANKING
            )
            ORDER BY PROJECT_ID, RANKING
            """

        project_info_df = pd.read_sql(text(sql_project_info), db.bind)
        project_content_df = pd.read_sql(text(sql_project_content), db.bind)
        project_df = project_info_df.merge(project_content_df, on="project_id", how="left")
        freelancer_df = pd.read_sql(text(sql_freelancer), db.bind)
        inter_df = pd.read_sql(text(sql_inter), db.bind)
        inter_implicit_df = pd.read_sql(text(sql_inter_implicit), db.bind)

        check_path(data_path)
        project_df.to_csv(os.path.join(data_path, "project.csv"), index=False)
        freelancer_df.to_csv(os.path.join(data_path, "freelancer.csv"), index=False)
        inter_df.to_csv(os.path.join(data_path, "inter.csv"), index=False)
        inter_implicit_df.to_csv(os.path.join(data_path, "inter_implicit.csv"), index=False)

    except Exception as e:
        print(f"데이터 로드 중 오류 발생: {e}")

    finally:
        db.close()


def preprocess_data(
        data_path: str, 
        n_components: int, 
        embed: bool = False, 
        similarity: Optional[str] = None
    ) -> Optional[Union[np.ndarray, torch.Tensor]]:
    """
    데이터 전처리 함수

    Args:
        data_path (str): 데이터 저장 경로
        n_components (int): 텍스트 임베딩 벡터에 사용할 PCA 주성분 개수
        embed (bool): 전처리 방식. 임베딩을 사용할 경우 True. 기본값은 False (인코딩)
        similarity (Optional[str]): 유사도를 추가 피처로 사용할 경우 종류 선택. 기본값은 None
                                    ("cosine", "dot_product", "elementwise_product", "jaccard")
    
    Returns:
        Optional[Union[np.ndarray, torch.Tensor]]: similarity를 선택하면 유사도 출력. 기본값은 None
    """
    project_df = pd.read_csv(os.path.join(data_path, "project.csv"))
    freelancer_df = pd.read_csv(os.path.join(data_path, "freelancer.csv"))

    print("📍 preprocessing project data ==============================")
    # 텍스트 임베딩 (Upstage Embeddings -> PCA)
    project_df = Preprocessing.text_embedding(project_df, "project_content", n_components)
    
    # 범주형 변수 인코딩 (멀티-핫)
    project_df = Preprocessing.encode_categorical_features(
        project_df, 
        categorical_cols=["category_id", "skill_id"]
    )

    if embed:
        project_category_df = project_df.iloc[:, 6:16]
        project_skill_df = project_df.iloc[:, 16:]
        
        # 범주형 변수 임베딩 (torch.nn.Embedding)
        project_category_df = Preprocessing.embed_categorical_features(
            project_category_df, 
            num_features=project_category_df.shape[1],
            embedding_dim=16,
            name="project",
            feature="category",
        )
        project_skill_df = Preprocessing.embed_categorical_features(
            project_skill_df, 
            num_features=project_skill_df.shape[1], 
            embedding_dim=16,
            name="project",
            feature="skill",
        )

        # 기존 인코딩 변수 제거 후 임베딩 변수 추가
        project_df = project_df.drop(columns=project_df.columns[6:])
        project_df = pd.concat([project_df, project_category_df, project_skill_df], axis=1)

    print("📍 preprocessing freelancer data ===========================")
    # 범주형 변수 인코딩 (멀티-핫)
    freelancer_df = Preprocessing.encode_categorical_features(
        freelancer_df, 
        categorical_cols=["category_id", "skill_id"], 
        skill_col="skill_id",
        expertise_col="skill_temp"
    )

    if embed:
        freelancer_category_df = freelancer_df.iloc[:, 3:13]
        freelancer_skill_df = freelancer_df.iloc[:, 13:]
        
        # 범주형 변수 임베딩 (torch.nn.Embedding)
        freelancer_category_df = Preprocessing.embed_categorical_features(
            freelancer_category_df,
            num_features=freelancer_category_df.shape[1], 
            embedding_dim=16,
            name="freelancer",
            feature="category",
        )
        freelancer_skill_df = Preprocessing.embed_categorical_features(
            freelancer_skill_df,
            num_features=freelancer_skill_df.shape[1], 
            embedding_dim=16,
            name="freelancer",
            feature="skill",
            weight=True
        )

        # 기존 인코딩 변수 제거 후 임베딩 변수 추가
        freelancer_df = freelancer_df.drop(columns=freelancer_df.columns[3:])
        freelancer_df = pd.concat([freelancer_df, freelancer_category_df, freelancer_skill_df], axis=1)

    project_df.to_csv(os.path.join(data_path, "project.csv"), index=False)
    freelancer_df.to_csv(os.path.join(data_path, "freelancer.csv"), index=False)

    # 유사도 계산 (인코딩/임베딩 둘 다 사용 가능. 단, 자카드 유사도는 인코딩만 사용 가능)
    match similarity:
        case "cosine":
            print(f"📍 calculating {similarity} similiarities ==============================")
            category_similarity = Preprocessing.calculate_similarity_matrix(
                project_category_df,
                freelancer_category_df,
                method="cosine"
            )
            skill_similarity = Preprocessing.calculate_similarity_matrix(
                project_skill_df,
                freelancer_skill_df,
                method="cosine"
            )

            return category_similarity, skill_similarity
        
        case "dot_product":
            print(f"📍 calculating {similarity} similiarities ==============================")
            category_similarity = Preprocessing.calculate_similarity_matrix(
                project_category_df,
                freelancer_category_df,
                method="dot_product"
            )
            skill_similarity = Preprocessing.calculate_similarity_matrix(
                project_skill_df,
                freelancer_skill_df,
                method="dot_product"
            )

            return category_similarity, skill_similarity
        
        case "elementwise_product":
            print(f"📍 calculating {similarity} similiarities ==============================")
            category_similarity = Preprocessing.calculate_similarity_matrix(
                project_category_df,
                freelancer_category_df,
                method="elementwise_product"
            )
            skill_similarity = Preprocessing.calculate_similarity_matrix(
                project_skill_df,
                freelancer_skill_df,
                method="elementwise_product"
            )

            return category_similarity, skill_similarity
        
        case "jaccard":
            print(f"📍 calculating {similarity} similiarities ==============================")
            category_similarity = Preprocessing.calculate_similarity_matrix(
                project_category_df,
                freelancer_category_df,
                method="jaccard"
            )
            skill_similarity = Preprocessing.calculate_similarity_matrix(
                project_skill_df,
                freelancer_skill_df,
                method="jaccard"
            )

            return category_similarity, skill_similarity
        
        case _: 
            raise ValueError("Invalid input: Similarity should be 'cosine', 'dot_product', 'elementwise-product' and 'jaccard'.")
