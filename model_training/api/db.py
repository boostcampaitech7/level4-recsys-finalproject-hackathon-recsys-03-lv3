import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, sessionmaker
import cx_Oracle

# .env 파일 로드
load_dotenv()

# 환경 변수에서 Wallet 및 라이브러리 경로 가져오기
TNS_ADMIN = os.getenv("TNS_ADMIN")
# ORA_LIBRARY_PATH = os.getenv("ORA_LIBRARY_PATH")
ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")

# cx_Oracle Instant Client 초기화
# cx_Oracle.init_oracle_client(lib_dir=ORA_LIBRARY_PATH, config_dir=TNS_ADMIN)

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