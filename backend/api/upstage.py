import os
import json
import numpy as np
import pickle
from typing import List, Dict

from dotenv import load_dotenv
from openai import OpenAI
from langchain_upstage import UpstageEmbeddings

from src.utils.utils import download_model_file

load_dotenv()
UPSTAGE_TOKEN = os.getenv("UPSTAGE_TOKEN")

client = OpenAI(
    api_key=UPSTAGE_TOKEN,
    base_url="https://api.upstage.ai/v1/solar"
)
embedding = UpstageEmbeddings(api_key=UPSTAGE_TOKEN, model="embedding-passage")


def chat_with_solar(messages: List[Dict]) -> Dict:
    """
    Solar AI 모델과 대화하는 함수

    Args:
        messages (List[Dict):
            - OpenAI API 형식의 메시지 리스트.
            - 각 메시지는 {"role": "user" | "assistant" | "system", "content": "message"} 형식.

    Returns:
        Dict: 모델의 응답 메세지
    """
    response = client.chat.completions.create(
        model="solar-pro",
        messages=messages,
        temperature=0.0  # 같은 프롬프트에 대해 항상 유사한 출력
    )
    return json.loads(response.choices[0].message.content)


def text_embedding(
    text: str
) -> np.ndarray:
    """
    Upstage Embeddings을 활용해 텍스트 데이터를 임베딩 후 PCA로 차원을 축소하는 함수

    Args
        text (str): 임베딩할 텍스트

    Returns:
        np.ndarray: PCA 변환된 벡터
    """
    # 텍스트 임베딩
    embed_result = np.array(embedding.embed_documents([text])[0])

    # 저장된 Scaler & PCA 모델 로드
    scaler_file = download_model_file(file_name="scaler.pkl")
    pca_file = download_model_file(file_name="pca.pkl")

    with open(scaler_file, "rb") as f:
        scaler = pickle.load(f)

    with open(pca_file, "rb") as f:
        pca = pickle.load(f)

    # 저장된 Scaler로 데이터 정규화
    X_scaled = scaler.transform(embed_result.reshape(1, -1))

    # 저장된 PCA 모델로 차원 축소
    X_pca = pca.transform(X_scaled)

    return X_pca.flatten()
