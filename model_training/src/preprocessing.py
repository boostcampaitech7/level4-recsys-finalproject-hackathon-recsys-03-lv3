import json
import os

import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from tqdm import tqdm
from dotenv import load_dotenv
from langchain_upstage import UpstageEmbeddings
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from typing import List, Optional, Set, Union


class Preprocessing:
    def text_embedding(
        df: pd.DataFrame,
        col_name: str,
        n_components: int
    ) -> pd.DataFrame:
        """
        텍스트 데이터를 임베딩 후 PCA로 차원 축소를 적용하는 함수 (Upstage Embeddings 사용)

        Args
            df (pd.DataFrame): 임베딩할 텍스트 컬럼이 있는 데이터프레임
            col_name (str): 임베딩할 텍스트 컬럼명
            n_components (int): 텍스트 임베딩 벡터에 사용할 PCA 주성분 개수

        Returns:
            pd.DataFrame: 최종 임베딩된 텍스트 컬럼이 포함된 데이터프레임
        """
        load_dotenv()
        UPSTAGE_TOKEN = os.getenv("UPSTAGE_TOKEN")

        embeddings = UpstageEmbeddings(api_key=UPSTAGE_TOKEN, model="embedding-passage")

        embed_results = embeddings.embed_documents(df[col_name].tolist())
        embed_col = pd.DataFrame(np.array(embed_results))

        # 데이터 표준화 및 PCA 적용
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(embed_col)

        pca = PCA(n_components=n_components, random_state=42)
        X_pca = pca.fit_transform(X_scaled)

        # 새로운 컬럼 이름 생성 후 변경 (예: project_content_0, project_content_1, ...)
        X_pca_df = pd.DataFrame(
            X_pca,
            columns=[f"{col_name}_{i}" for i in range(n_components)]
        )

        # 원본 데이터프레임에 PCA 결과 병합
        result_df = pd.concat([df, X_pca_df], axis=1).drop(columns=[col_name])

        return result_df

    def encode_categorical_features(
        df: pd.DataFrame,
        categorical_cols: List[str],
        skill_col: Optional[str] = None,
        expertise_col: Optional[str] = None
    ) -> pd.DataFrame:
        """
        주어진 범주형 변수를 멀티-핫 인코딩하고, 프리랜서 스킬의 경우 스킬 숙련도까지 반영하는 함수

        Args:
            df (pd.DataFrame): 프리랜서/프로젝트 데이터프레임
            categorical_cols (List[str]): 멀티-핫 인코딩을 적용할 모든 범주형 변수 리스트 (예: ["category_id", "skill_id"])
            skill_col (Optional[str]): 프리랜서 스킬 변수명. 프리랜서의 스킬에 가중치를 적용하고 싶을 때 사용한다. 기본값은 None (예: "skill_id")
            expertise_col (Optional[str]): 리랜서 스킬 숙련도 변수명. 프리랜서 스킬의 가중치로 사용한다. 기본값은 None (예: "skill_temp")

        Returns:
            pd.DataFrame: 범주형 변수에 멀티-핫 인코딩을 적용한 데이터프레임
        """
        # 범주형 변수 중 문자열로 리스트로 변환
        for col in categorical_cols + ([expertise_col] if expertise_col else []):
            if df[col].dtype == object:
                df[col] = df[col].apply(json.loads)

        # 범주형 변수 중 int로 저장된 값이 있으면 리스트로 변환
        for col in categorical_cols:
            if df[col].dtype == int:
                df[col] = df[col].apply(lambda x: [x])

        # 멀티-핫 벡터의 차원이 될 각 범주형 컬럼의 유니크한 값 저장
        all_unique_values = {col: np.unique(np.concatenate(df[col].values)) for col in categorical_cols}

        # 멀티-핫 벡터로 변환 (프리랜서 스킬에 숙련도를 반영하고 싶은 경우 따로 처리)
        def multi_hot_encode(values: List[int], all_values: np.ndarray) -> np.ndarray:
            return np.isin(all_values, values).astype(int)  # True → 1 변환

        def multi_hot_with_expertise(skill_list: List[int], skill_temp_list: List[int], skill_set: Set[int]) -> List[int]:
            skill_dict = dict(zip(skill_list, skill_temp_list))  # {skill_id: 숙련도} 딕셔너리 생성
            return np.array([skill_dict.get(skill, 0) for skill in skill_set])  # 존재하는 스킬만 숙련도 값, 없으면 0

        encoded_dfs = []
        for col in categorical_cols:
            all_values = np.array(all_unique_values[col])  # 연산 속도 개선을 위해 넘파이 배열로 변환
            if col == skill_col and expertise_col:
                encoded_matrix = np.vstack(df.apply(lambda row: multi_hot_with_expertise(row[col], row[expertise_col], all_values), axis=1))
            else:
                encoded_matrix = np.vstack(df[col].apply(lambda x: multi_hot_encode(x, all_values)))

            encoded_df = pd.DataFrame(encoded_matrix, columns=[f"{col}_{v}" for v in all_values])
            encoded_dfs.append(encoded_df)

        # 모든 인코딩된 데이터프레임을 원본과 결합
        result_df = pd.concat([df.drop(columns=categorical_cols + ([expertise_col] if expertise_col else []))] + encoded_dfs, axis=1)

        return result_df

    def embed_categorical_features(
        df: pd.DataFrame,
        num_features: int,
        embedding_dim: int,
        name: str = None,
        feature: str = None,
        weight: bool = False
    ) -> pd.DataFrame:
        """
        멀티-핫 인코딩된 범주형 데이터를 임베딩하는 함수 (torch.nn.Embedding 사용)

        Args:
            df (pd.DataFrame): 멀티-핫 인코딩된 범주형 데이터
            num_embeddings (int): 임베딩 레이어의 입력 차원 (범주 개수)
            embedding_dim (int): 임베딩 레이어의 출력 차원
            name (str, optional): 임베딩된 데이터프레임의 열에 들어갈 이름. 기본값은 None (예: freelancer, project)
            feature (str, optional): 임베딩된 데이터프레임의 열에 들어갈 피처 이름. 기본값은 None (예: category, skill)
            weight (bool, optional): 스킬 숙련도를 가중치로 사용할 지 여부. 기본값은 False

        Returns:
            pd.DataFrame: 임베딩 벡터의 각 차원을 열로 갖는 데이터프레임
        """
        # 멀티-핫 벡터를 텐서로 변환
        multi_hot_vectors = torch.tensor(df.to_numpy(), dtype=torch.float32)  # (batch_size, num_features)

        # 범주별 임베딩 벡터 생성
        embedding_layer = nn.Embedding(num_features, embedding_dim)

        # 임베딩 벡터 추출 (batch_size, num_features, embedding_dim)
        embedded_vectors = embedding_layer(torch.arange(num_features))

        # 스킬 숙련도를 가중치로 사용
        if weight:
            embedded_result = multi_hot_vectors.unsqueeze(-1) * embedded_vectors
            weights = multi_hot_vectors / (multi_hot_vectors.sum(dim=1, keepdim=True) + 1e-8)  # 가중치 계산
            embedded_result = (embedded_result * weights.unsqueeze(-1)).sum(dim=1)  # 가중 평균 풀링 (batch_size, embedding_dim)
        else:
            embedded_result = (multi_hot_vectors > 0).unsqueeze(-1) * embedded_vectors  # 0 또는 1 처리
            embedded_result = embedded_result.mean(dim=1)  # 평균 풀링 (batch_size, embedding_dim)

        embedded_array = embedded_result.detach().cpu().numpy()  # 텐서를 다시 넘파이 배열로 변환

        if name not in {"freelancer", "project"} and feature not in {"category", "skill"}:
            raise ValueError("Invalid input: name should be 'freelancer' or 'project' and feature should be 'category' or 'skill'")
        else:
            embedding_df = pd.DataFrame(
                embedded_array,
                columns=[f"{name}_{feature}_embedding_{i+1}" for i in range(embedded_array.shape[1])]
            )
            return embedding_df

    def calculate_similarity_matrix(
        matrix_1: Union[pd.DataFrame, np.ndarray],
        matrix_2: Union[pd.DataFrame, np.ndarray],
        method: Optional[str] = None,
        batch_size: int = 500
    ) -> pd.DataFrame:
        """
        두 행렬 간 유사도를 계산하는 함수. 메모리 최적화를 위해 배치 단위로 계산을 진행한다.

        Args:
            matrix_1 (Union[pd.DataFrame, np.ndarray]): 첫 번째 행렬
            matrix_2 (Union[pd.DataFrame, np.ndarray]): 두 번째 행렬
            method (Optional[str]): 유사도 계산 방법 ("cosine", "dot_product", "jaccard"). 기본값은 None
            batch_size (int): 계산에 사용할 배치 크기. 기본값은 500
        Returns:
            pd.DataFrame: 계산된 유사도 데이터프레임
        """
        matrix_1 = np.array(matrix_1)
        matrix_2 = np.array(matrix_2)
        similarity_matrix = np.zeros((matrix_1.shape[0], matrix_2.shape[0]))
        
        # tqdm 적용 (프로그레스 바)
        total_batches = (matrix_1.shape[0] // batch_size + 1) * (matrix_2.shape[0] // batch_size + 1)
        progress_bar = tqdm(total=total_batches, desc=f"Calculating {method} similarity", unit="batch")

        for i in range(0, matrix_1.shape[0], batch_size):
            end_i = min(i + batch_size, matrix_1.shape[0])
            
            for j in range(0, matrix_2.shape[0], batch_size):
                end_j = min(j + batch_size, matrix_2.shape[0])

                batch_1 = matrix_1[i:end_i]
                batch_2 = matrix_2[j:end_j]

                match method:
                    case "cosine":
                        similarity_matrix[i:end_i, j:end_j] = cosine_similarity(batch_1, batch_2)

                    case "dot_product":
                        similarity_matrix[i:end_i, j:end_j] = np.dot(batch_1, batch_2.T)

                    # 단, 자카드 유사도는 임베딩 벡터가 아니라 인코딩 벡터일 때 이용해야 한다.
                    case "jaccard":
                        # 두 행렬에서 0이 아닌 값을 모두 1로 변환
                        # 숙련도 값이 존재하는 경우, 스킬이 있다는 정보만 유지하여 1로 처리한다.
                        batch_1 = (batch_1 > 0).astype(int)
                        batch_2 = (batch_2 > 0).astype(int)

                        intersection = np.bitwise_and(batch_1[:, np.newaxis, :], batch_2[np.newaxis, :, :]).sum(axis=2)
                        union = np.bitwise_or(batch_1[:, np.newaxis, :], batch_2[np.newaxis, :, :]).sum(axis=2)
                        similarity_matrix[i:end_i, j:end_j] = intersection / (union + 1e-8)

                    case _:
                        raise ValueError(f"Unsupported method: {method}")

                progress_bar.update(1)

        progress_bar.close()
        return pd.DataFrame(similarity_matrix)
