from fastapi import HTTPException
from sqlalchemy import union_all, literal
from sqlalchemy.orm import Session


from src.models import Freelancer, Company, FreelancerCategory, FreelancerSkill
from src.schemas.auth import LoginResponse, FreelancerRegisterRequest, CompanyRegisterRequest
from src.utils.user_handler import verify_password, create_jwt_token, hash_password
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
            Freelancer.password.label("password"),
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
            "userId": user.id,
            "userName": user.name,
            "userType": user.type,
        }
        token = create_jwt_token(session_data)

        # 응답 데이터 반환
        return LoginResponse(
            token=token,
            userId=user.id,
            userName=user.name,
            userType=user.type,
        )

    def register_freelancer(db: Session, freelancer_data: FreelancerRegisterRequest) -> dict:
        """
        프리랜서 회원가입을 처리하는 메서드

        Args:
            db (Session): SQLAlchemy 세션 객체
            freelancer_data (FreelancerRegisterRequest): 프리랜서 회원가입 요청 데이터
        """
        # 이메일 중복 검사
        existing_freelancer = db.query(Freelancer).filter(Freelancer.email == freelancer_data.email).first()
        if existing_freelancer:
            raise HTTPException(
                status_code=ERROR_MESSAGES["CONFLICT"]["status"],
                detail=ERROR_MESSAGES["CONFLICT"]["message"].format("이미 존재하는 이메일입니다."),
            )

        # 비밀번호 해싱
        hashed_password = hash_password(freelancer_data.password)

        # 프리랜서 정보 저장
        new_freelancer = Freelancer(
            name=freelancer_data.freelancerName,
            email=freelancer_data.email,
            password=hashed_password,
            work_exp=freelancer_data.workExp,
            price=freelancer_data.price,
            work_type=freelancer_data.workType,
            role=freelancer_data.role,
            content=freelancer_data.freelancerContent,
            location_id=freelancer_data.locationId,
        )
        db.add(new_freelancer)
        db.commit()
        db.refresh(new_freelancer)

        # 카테고리 매핑 저장
        category_entries = [FreelancerCategory(freelancer_id=new_freelancer.id, category_id=category_id) for category_id in freelancer_data.categoryList]
        db.bulk_save_objects(category_entries)

        # 스킬 매핑 저장 (기본 점수 2.0)
        skill_entries = [FreelancerSkill(freelancer_id=new_freelancer.id, skill_id=skill_id, skill_score=2.0) for skill_id in freelancer_data.skillList]
        db.bulk_save_objects(skill_entries)

        db.commit()

    def register_company(db: Session, company_data: CompanyRegisterRequest):
        """
        기업 회원가입을 처리하는 메서드

        Args:
            db (Session): SQLAlchemy 세션 객체
            company_data (CompanyRegisterRequest): 기업 회원가입 요청 데이터
        """
        # 이메일 중복 검사
        existing_company = db.query(Company).filter(Company.email == company_data.email).first()
        if existing_company:
            raise HTTPException(
                status_code=ERROR_MESSAGES["CONFLICT"]["status"],
                detail=ERROR_MESSAGES["CONFLICT"]["message"].format("이미 존재하는 이메일입니다."),
            )

        # 비밀번호 해싱
        hashed_password = hash_password(company_data.password)

        # 기업 정보 저장
        new_company = Company(
            name=company_data.companyName,
            email=company_data.email,
            content=company_data.companyContent,
            password=hashed_password,
            location_id=company_data.locationId,
        )
        db.add(new_company)
        db.commit()
