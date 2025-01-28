import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# .env 파일 로드
load_dotenv()

# 환경 변수에서 Oracle 설정 가져오기
TNS_ADMIN = os.getenv("TNS_ADMIN")  # Oracle Wallet 경로
ORACLE_USER = os.getenv("ORACLE_USER")  # Oracle 사용자 이름
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")  # Oracle 비밀번호

# SQLAlchemy 연결 URL 생성
DATABASE_URL = f"oracle+cx_oracle://{ORACLE_USER}:{ORACLE_PASSWORD}@hrmonydb_high"

# SQLAlchemy 엔진 및 세션 생성
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    데이터베이스 세션을 생성하고, 요청 종료 시 닫음
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
