import argparse
from huggingface_hub import HfApi, HfFolder
from omegaconf import OmegaConf


def upload_model(
    local_model_path: str,
    repo_name: str,
    file_name: str = None,
    upload_name: str = None
):
    """
    HTTP 기반 업로드 방식으로 Hugging Face Hub에 모델 업로드

    Args:
        local_model_path (str): 로컬 모델 디렉토리 경로
        repo_name (str): Hugging Face 저장소 이름
        file_name (str, optional): 업로드할 파일명. None일 경우 전체 폴더를 업로드
    """
    try:
        # Hugging Face Hub 인증 토큰 가져오기
        token = HfFolder.get_token()
        if token is None:
            raise ValueError("토큰 정보가 없습니다. `huggingface-cli login`를 먼저 사용해 로그인하세요.")

        # API를 사용하여 모델 업로드
        api = HfApi()

        # 단일 파일 업로드
        if file_name:
            api.upload_file(
                path_or_fileobj=f"{local_model_path}/{file_name}",
                path_in_repo=file_name,
                repo_id=repo_name,
                repo_type="model",
                token=token
            )

        # 전체 파일 업로드
        else:
            api.upload_folder(
                folder_path=local_model_path,
                repo_id=repo_name,
                repo_type="model",
                token=token
            )

        print(f"https://huggingface.co/{repo_name}에 모델이 성공적으로 저장되었습니다.")
    except Exception as e:
        print(f"Failed to upload model: {e}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    arg = parser.add_argument

    arg(
        "--config",
        "-c",
        help="Configuration 파일을 설정합니다.",
        default="config/config.yaml"
    )
    arg(
        "--file",
        "-f",
        help="업로드할 파일의 파일명을 입력합니다. (폴더명 이후 경로 입력 ex.EASE-Jan-28-2025_15-26-45.pth)",
        default=None
    )

    args = parser.parse_args()

    config_args = OmegaConf.create(vars(args))
    config_yaml = OmegaConf.load(args.config)

    # args에 있는 값이 config_yaml에 있는 값보다 우선함. (단, None이 아닌 값일 경우)
    for key in config_args.keys():
        if config_args[key] is not None:
            config_yaml[key] = config_args[key]

    args = config_yaml

    upload_model(
        local_model_path=args.output_path,
        repo_name=args.repo_name,
        file_name=args.file
    )
