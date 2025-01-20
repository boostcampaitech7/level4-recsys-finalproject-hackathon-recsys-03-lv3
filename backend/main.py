import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.request_route import request as request_router
from src.routes.receive_route import receive as receive_router
from src.routes.user_route import user as user_router

# FastAPI 앱 초기화
app = FastAPI(
    title="HRmony",
    description="AI 기반 추천 시스템을 활용해 팀 협업과 프로젝트 매칭을 지원하는 HR 플랫폼",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 서버 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello, React!"}

# 라우터 등록
app.include_router(request_router, prefix="/api/request", tags=["Request"])
app.include_router(receive_router, prefix="/api/receive", tags=["Receive"])
app.include_router(user_router, prefix="/api/user", tags=["User"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)