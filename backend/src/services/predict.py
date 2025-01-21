from huggingface_hub import hf_hub_download


def download_model_file(repo_name: str, file_name: str, save_dir: str = "./model") -> str:
    """
    Hugging Face Hub에서 특정 파일 다운로드.

    Args:
        repo_name (str): Hugging Face 저장소 이름.
        file_name (str): 다운로드할 파일 이름.
        save_dir (str): 파일을 저장할 로컬 디렉토리 경로.
    """
    try:
        # 파일 다운로드
        file_path = hf_hub_download(
            repo_id=repo_name,
            filename=file_name,
            cache_dir=save_dir,
            use_auth_token=True
        )
        print(f"Downloaded {file_name} to {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download file: {e}")


repo_name = "TaroSin/HRmony"
file_name = "model.pkl"
file_path = download_model_file(repo_name, file_name)
