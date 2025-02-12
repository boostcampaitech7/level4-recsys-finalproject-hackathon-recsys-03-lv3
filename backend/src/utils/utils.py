import json
from typing import Union, List
from huggingface_hub import hf_hub_download


def parse_json_to_list(value: str) -> List[Union[int, float, str]]:
    """
    주어진 값이 문자열이면 JSON으로 파싱하여 리스트로 변환

    Args:
        value (str): 파싱할 값 (보통 JSON 문자열)

    Returns:
        List[Union[int, str]]: JSON 파싱에 성공하면 리스트, 실패하면 빈 리스트
    """
    try:
        return json.loads(value)
    except Exception:
        return []  # 변환 실패 시 빈 리스트 반환


def download_model_file(
    file_name: str,
    save_dir: str = "./model"
) -> str:
    """
    Hugging Face Hub에서 특정 파일 다운로드.

    Args:
        file_name (str): 다운로드할 파일 이름.
        save_dir (str): 파일을 저장할 로컬 디렉토리 경로.
    """
    try:
        # 파일 다운로드
        file_path = hf_hub_download(
            repo_id="TaroSin/HRmony",
            filename=file_name,
            cache_dir=save_dir,
            use_auth_token=True
        )
        print(f"Downloaded {file_name} to {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download file: {e}")
