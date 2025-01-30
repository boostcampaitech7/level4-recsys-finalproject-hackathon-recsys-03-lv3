from fastapi import HTTPException
from sqlalchemy import union_all, literal
from sqlalchemy.orm import Session

from src.models import Freelancer, Company
from src.schemas.auth import LoginResponse
from src.utils.user_handler import verify_password, create_jwt_token
from src.utils.error_messages import ERROR_MESSAGES


class AuthService:
    def login_user(db: Session, email: str, password: str) -> LoginResponse:
        """
        사용자 로그인 기능

        Args:
            db (Session): SQLAlchemy 데이터베이스 세션
            email (str): 사용자의 이메일 주소
            password (str): 사용자의 비밀번호

        Returns:
            LoginResponse: 사용자 정보와 인증 토큰을 포함한 응답 데이터
        """
        if not email or not password:
            raise HTTPException(
                status_code=ERROR_MESSAGES["BAD_REQUEST"]["status"],
                detail=ERROR_MESSAGES["BAD_REQUEST"]["message"].format("이메일 또는 비밀번호")
            )

        freelancer_query = db.query(
            Freelancer.id.label("id"),
            Freelancer.name.label("name"),
            Company.password.label("password"),
            literal(0).label("type"),
        ).filter(Freelancer.email == email)

        company_query = db.query(
            Company.id.label("id"),
            Company.name.label("name"),
            Company.password.label("password"),
            literal(1).label("type"),
        ).filter(Company.email == email)

        union_query = union_all(freelancer_query, company_query)
        user = db.execute(union_query).fetchone()

        if not user:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format("사용자 정보")
            )

        # 비밀번호 검증
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=ERROR_MESSAGES["UNAUTHORIZED"]["status"],
                detail=ERROR_MESSAGES["UNAUTHORIZED"]["message"]
            )

        # JWT 토큰 생성
        session_data = {
            "user_id": user.id,
            "user_name": user.name,
            "user_type": user.type,
        }
        token = create_jwt_token(session_data)

        # 응답 데이터 반환
        return LoginResponse(
            token=token,
            user_id=user.id,
            user_name=user.name,
            user_type=user.type,
        )
