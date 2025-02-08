# Python 3.10 사용
FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    libaio1 unzip curl && \
    rm -rf /var/lib/apt/lists/*

# Oracle Instant Client 복사 및 압축 해제
COPY backend/instantclient/instantclient-basic-linux.x64-23.6.0.24.10.zip /opt/oracle/
RUN mkdir -p /usr/lib/oracle/instantclient && \
    unzip /opt/oracle/instantclient-basic-linux.x64-23.6.0.24.10.zip -d /usr/lib/oracle/instantclient/ && \
    rm /opt/oracle/instantclient-basic-linux.x64-23.6.0.24.10.zip

# 환경 변수 설정
ENV LD_LIBRARY_PATH="/usr/lib/oracle/instantclient/instantclient_23_6:${LD_LIBRARY_PATH}"
ENV ORACLE_HOME="/usr/lib/oracle/instantclient/instantclient_23_6"
ENV PATH="${ORACLE_HOME}:${PATH}"

# requirements.txt 복사 및 설치
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 애플리케이션 코드 복사
COPY backend/ ./

# FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
