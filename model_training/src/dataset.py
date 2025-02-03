import os
import pandas as pd
import json

from sqlalchemy import text
from dotenv import load_dotenv
from langchain_upstage import UpstageEmbeddings
from typing import Tuple, List, Dict
from sklearn.preprocessing import MultiLabelBinarizer

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
        sql_project_info = """
            SELECT  P.PROJECT_ID AS project_id,
                    P.DURATION AS duration,
                    P.BUDGET AS budget,
                    P.PRIORITY AS priority,
                    P.COMPANY_ID AS company_id,
                    (SELECT JSON_ARRAYAGG(PC.CATEGORY_ID)
                    FROM PROJECT PC
                    WHERE PC.PROJECT_ID = P.PROJECT_ID) AS category_id,
                    C.CATEGORY_NAME AS category_name,
                    (SELECT JSON_ARRAYAGG(PS.SKILL_ID)
                    FROM PROJECT_SKILL PS
                    WHERE PS.PROJECT_ID = P.PROJECT_ID) AS skill_id,
                    P.FREELANCER_ID AS freelancer_id
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
                    F.PRICE AS price,
                    (SELECT JSON_ARRAYAGG(FS.SKILL_ID) AS SKILL_ID
                     FROM FREELANCER_SKILL FS
                     WHERE FS.FREELANCER_ID = F.FREELANCER_ID) AS skill_id,
                    (SELECT JSON_ARRAYAGG(FS.SKILL_ID) AS SKILL_TEMP
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
                        MATCHING_SCORE,
                        ROW_NUMBER() OVER (PARTITION BY PROJECT_ID ORDER BY MATCHING_SCORE DESC) AS RANKING
                FROM    PROJECT_RANKING
            )
            """

        project_info_df = pd.read_sql(text(sql_project_info), db.bind)
        project_content_df = pd.read_sql(text(sql_project_content), db.bind)
        project_df = project_info_df.merge(project_content_df, on="project_id", how="left")
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


def preprocess_data(data_path: str):
    """
    데이터 전처리 함수

    Args:
        data_path (str): 데이터 저장 경로
    """
    project_df = pd.read_csv(os.path.join(data_path, "project.csv"))
    freelancer_df = pd.read_csv(os.path.join(data_path, "freelancer.csv"))
    project_df = project_df.head(5)
    freelancer_df = freelancer_df.head(5)

    print("📍 preprocessing project ==============================")
    project_df = Preprocessing.text_embedding(project_df, "project_content")

    print("📍 preprocessing freelancer ===========================")

    project_df.to_csv(os.path.join(data_path, "project_test.csv"), index=False)
    freelancer_df.to_csv(os.path.join(data_path, "freelancer_test.csv"), index=False)


class Preprocessing:
    def text_embedding(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
        """
        텍스트 임베딩 함수 (Upstage Embeddings 사용)

        Args
            df (pd.DataFrame): 임베딩할 텍스트 컬럼이 있는 데이터프레임
            col_name (str): 임베딩할 텍스트 컬럼명

        Returns:
            pd.DataFrame: 임베딩된 텍스트 컬럼이 포함된 데이터프레임
        """
        load_dotenv()
        UPSTAGE_TOKEN = os.getenv("UPSTAGE_TOKEN")

        embeddings = UpstageEmbeddings(
            api_key=UPSTAGE_TOKEN,
            model="embedding-passage"
        )

        emb_results = embeddings.embed_documents(df[col_name].tolist())
        df[col_name] = emb_results

        return df

    def parse_column(value: str) -> Tuple[List[str], Dict[str, float]]:
        """
        JSON 형태 또는 리스트 형태의 문자열 데이터를 파싱하여 리스트로 변환하는 함수.

        Args:
            value(str) : JSON 문자열 또는 리스트 문자열

        Returns:
            list : 변환된 리스트
            dict : 가중치 딕셔너리 (프리랜서 skill_id만 해당, 없으면 빈 딕셔너리)
        """
        parsed_list = []
        weights = {}

        try:
            parsed = json.loads(value.replace("'", '"')) if "{" in value else eval(value)

            if isinstance(parsed, list):
                if all(isinstance(item, dict) for item in parsed):
                    for skill in parsed:
                        parsed_list.append(skill["skill_id"])
                        weights[skill["skill_id"]] = skill.get("skill_score", 1)
                else:
                    parsed_list = parsed
        except (json.JSONDecodeError, SyntaxError, TypeError):
            pass

        return parsed_list, weights

    def multi_hot_encoding(
            df: pd.DataFrame,
            label_col: str,
            pivot_col: str,
            weight_col: str = None
    ) -> pd.DataFrame:
        """
        프로젝트 및 프리랜서의 스킬을 멀티-핫 인코딩하는 함수
        (프리랜서의 경우 스킬 온도를 적용)

        Args:
            df (pd.DataFrame): pivot_col과 label_col을 포함하는 데이터프레임
            label_col (str): 멀티핫 인코딩할 스킬 컬럼명
            pivot_col (str): 그룹화할 기준이 되는 컬럼명 (project_id 또는 freelancer_id)
            weight_col (str, optional): 스킬 가중치를 적용할 경우 제공할 컬럼명 (프리랜서만 해당)

        Returns:
            pd.DataFrame: 멀티핫 인코딩(및 가중치 적용)이 완료된 데이터프레임 반환
        """

        # 스킬 컬럼을 리스트 형태로 변환
        df[["parsed_values", "parsed_weights"]] = df[label_col].apply(
            lambda x: pd.Series(Preprocessing.parse_column(str(x)))
        )

        # pivot_col별 "parsed_values"를 리스트로 묶기
        grouped_df = df.groupby(pivot_col)["parsed_values"].sum().reset_index()

        # MultiLabelBinarizer를 사용하여 멀티 핫 인코딩 수행
        mlb = MultiLabelBinarizer()
        multi_hot_encoded = mlb.fit_transform(grouped_df["parsed_values"])

        # 결과를 데이터프레임으로 변환
        multi_hot_df = pd.DataFrame(multi_hot_encoded, columns=mlb.classes_)
        multi_hot_df.insert(0, pivot_col, grouped_df[pivot_col])

        # 가중치 적용 (프리랜서 스킬 온도 적용)
        if weight_col and "parsed_weights" in df:
            weight_map = {
                row[pivot_col]: row["parsed_weights"] for _, row in df.iterrows()
            }
            for skill in mlb.classes_:
                if skill in multi_hot_df.columns:
                    multi_hot_df[skill] = multi_hot_df[pivot_col].map(
                        lambda x: weight_map.get(x, {}).get(skill, 1)
                    ) * multi_hot_df[skill]

        return multi_hot_df
