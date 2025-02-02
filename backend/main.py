import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.auth_route import auth as auth_router
from src.routes.filter_route import filter as filter_router
from src.routes.mymony_route import mymony as mymony_router
from src.routes.project_route import project as project_router
from src.routes.resource_route import resource as resource_router

# FastAPI 앱 초기화
app = FastAPI(
    title="HRmony",
    description="AI 기반 추천 시스템을 활용해 프리랜서와 프로젝트의 매칭을 지원하는 플랫폼",
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
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(filter_router, prefix="/api/filter", tags=["Filter"])
app.include_router(mymony_router, prefix="/api/mymony", tags=["Mymony"])
app.include_router(project_router, prefix="/api/project", tags=["Project"])
app.include_router(resource_router, prefix="/api/resource", tags=["Resource"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
