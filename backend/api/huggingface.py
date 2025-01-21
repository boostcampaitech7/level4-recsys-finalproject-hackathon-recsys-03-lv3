import os
from dotenv import load_dotenv
from huggingface_hub import HfFolder

# .env 파일 로드
load_dotenv()

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Hugging Face 토큰 저장
HfFolder.save_token(HUGGINGFACE_TOKEN)
