from huggingface_hub import HfApi, HfFolder

def upload_model(local_model_path: str, repo_name: str):
    """
    HTTP 기반 업로드 방식으로 Hugging Face Hub에 모델 업로드.

    Args:
        local_model_path (str): 로컬 모델 디렉토리 경로.
        repo_name (str): Hugging Face 저장소 이름.
    """
    try:
        # Hugging Face Hub 인증 토큰 가져오기
        token = HfFolder.get_token()
        if token is None:
            raise ValueError("No Hugging Face token found. Please log in using `huggingface-cli login`.")

        # API를 사용하여 모델 업로드
        api = HfApi()
        api.upload_folder(
            folder_path=local_model_path,
            repo_id=repo_name,
            repo_type="model",
            token=token
        )
        print(f"Model successfully uploaded to https://huggingface.co/{repo_name}")
    except Exception as e:
        print(f"Failed to upload model: {e}")
