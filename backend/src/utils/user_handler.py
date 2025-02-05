import os
import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer
from starlette.requests import Request

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


class AuthRequired(HTTPBearer):
    """
    HTTPBearer 인증을 처리하는 클래스
    (FastAPI의 HTTPBearer를 확장하여 Authorization 헤더를 검증하고, JWT 토큰을 디코딩하여 요청 상태에 사용자 정보를 추가)

    Args:
        HTTPBearer (bool): 인증 실패 시 자동으로 예외를 발생시킬지 여부
    """
    async def __call__(self, request: Request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise Exception("Authorization 헤더가 없습니다.")

        try:
            token_type, token = auth_header.split(" ")
            if token_type != "Bearer":
                raise Exception("Invalid token type in Authorization header.")
        except ValueError:
            raise Exception("Authorization 헤더가 잘못된 형식입니다.")

        if not isinstance(token, str):
            raise Exception(f"Invalid token type. Token must be a string. Got: {type(token)}")

        # 디코드된 정보를 상태에 저장
        request.state.token_info = decode_jwt_token(token)


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


def hash_password(password: str) -> str:
    """
    주어진 비밀번호를 bcrypt 알고리즘을 사용하여 해싱합니다.

    Args:
        password (str): 해싱할 비밀번호

    Returns:
        str: bcrypt 해싱된 비밀번호
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    return pwd_context.hash(password)