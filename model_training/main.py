from src.trainer import train_and_save_model
from src.utils import upload_model

if __name__ == "__main__":
    # 학습 및 로컬 저장
    output_dir = "./model_training/output"
    train_and_save_model(output_dir=output_dir)

    # Hugging Face Hub 업로드
    repo_name = "TaroSin/HRmony"
    upload_model(local_model_path=output_dir, repo_name=repo_name)
