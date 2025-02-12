from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db import get_db
from src.schemas.auth import LoginRequest, LoginResponse, FreelancerRegisterRequest, CompanyRegisterRequest
from src.services.auth_service import AuthService

auth = APIRouter()


@auth.post("/login", response_model=LoginResponse)
def login_user(user_data: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    """
    사용자 로그인 API

    Args:
        user_data (LoginRequest): 이메일과 비밀번호를 포함한 요청 데이터
        db (Session): SQLAlchemy 데이터베이스 세션

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


@auth.post("/register/freelancer")
def register_freelancer(
    freelancer_data: FreelancerRegisterRequest, db: Session = Depends(get_db)
):
    """
    프리랜서 회원가입 API

    프리랜서 계정을 생성하는 API로, 입력된 정보를 검증한 후 데이터베이스에 저장합니다.

    Args:
        freelancer_data (FreelancerRegisterRequest): 프리랜서 회원가입 요청 데이터
        db (Session): SQLAlchemy 세션 객체
    """
    AuthService.register_freelancer(db, freelancer_data)


@auth.post("/register/company")
def register_company(
    company_data: CompanyRegisterRequest, db: Session = Depends(get_db)
):
    """
    기업 회원가입 API

    기업 계정을 생성하는 API로, 입력된 정보를 검증한 후 데이터베이스에 저장합니다.

    Args:
        company_data (CompanyRegisterRequest): 기업 회원가입 요청 데이터
        db (Session): SQLAlchemy 세션 객체
    """
    AuthService.register_company(db, company_data)
