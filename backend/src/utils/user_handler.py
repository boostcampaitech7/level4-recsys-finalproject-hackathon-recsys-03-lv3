import os
import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timedelta


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def create_jwt_token(data: dict) -> str:
    """
    주어진 데이터를 기반으로 JWT 토큰을 생성

    Args:
        data (dict): 토큰에 포함할 사용자 데이터 (예: 사용자 ID, 이름 등)

    Returns:
        str: 생성된 JWT 토큰
    """
    # .env 파일 로드
    load_dotenv()

    expiration = datetime.now() + timedelta(hours=1)  # 1시간 후 만료
    payload = data.copy()
    payload.update({"exp": expiration})
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_jwt_token(token: str) -> dict:
    """
    JWT 토큰에서 사용자 데이터 추출

    Args:
        token (str): JWT 토큰

    Returns:
        dict: 토큰에 포함된 사용자 데이터 (예: 사용자 ID, 이름 등)
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("이미 만료된 토큰입니다.")
    except jwt.InvalidTokenError:
        raise Exception("유효하지 않은 토큰입니다.")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    입력된 비밀번호가 해싱된 비밀번호와 일치하는지 확인

    Args:
        plain_password (str): 사용자가 입력한 비밀번호
        hashed_password (str): 데이터베이스에 저장된 해싱된 비밀번호

    Returns:
        bool: 비밀번호가 일치하면 True, 그렇지 않으면 False
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    return pwd_context.verify(plain_password, hashed_password)
