import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# .env 파일 로드
load_dotenv()

# 환경 변수에서 Oracle 설정 가져오기
TNS_ADMIN = os.getenv("TNS_ADMIN")  # Oracle Wallet 경로
ORACLE_USER = os.getenv("ORACLE_USER")  # Oracle 사용자 이름
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")  # Oracle 비밀번호

# Oracle 데이터베이스 연결 URL
DATABASE_URL = f"oracle+cx_oracle://{ORACLE_USER}:{ORACLE_PASSWORD}@hrmonydb_high"

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_size=10,           # 커넥션 풀 크기
    max_overflow=20,        # 초과 허용 커넥션 수
    pool_timeout=30,        # 연결을 기다리는 최대 시간 (초)
    pool_recycle=3600,      # 1시간 마다 연결 재사용
    pool_pre_ping=True,     # 연결 체크 후 사용 (끊어진 연결 방지)
    echo=True
)

# Base 클래스 생성 (모델 정의에 사용)
Base = declarative_base()

# 세션 풀링 설정
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_db():
    """
    데이터베이스 세션을 생성하고, 요청 종료 시 닫음
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()  # 오류 발생 시 롤백
        raise
    finally:
        db.close()  # 연결을 닫지 않고 풀링에 반환
