from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.schemas.auth import LoginRequest, LoginResponse
from src.services.auth_service import AuthService
from api.db import get_db

auth = APIRouter()


@auth.post("/login", response_model=LoginResponse)
def login_user(user_data: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    """
    사용자 로그인 API

    Args:
        user_data (UserLoginRequest): 이메일과 비밀번호를 포함한 요청 데이터
        db (Session, optional): SQLAlchemy 데이터베이스 세션

    Returns:
        LoginResponse: 사용자 정보와 인증 토큰을 포함한 응답 데이터
    """
    try:
        return AuthService.login_user(db, user_data.email, user_data.password)
    except HTTPException as e:
        raise e


@auth.post("/logout")
def logout_user():
    """
    사용자 로그아웃 API
    (클라이언트에서 JWT 토큰 삭제)
    """
    pass
