from typing import List

from fastapi import APIRouter, Depends, Path, Query, HTTPException, Request
from sqlalchemy.orm import Session

from api.db import get_db
from src.schemas.project import ProjectListResponse, ProjectDetailResponse
from src.services.project_service import ProjectService
from src.utils.user_handler import AuthRequired
from src.utils.error_messages import ERROR_MESSAGES

project = APIRouter(
    dependencies=[Depends(AuthRequired())]
)


@project.get("/", response_model=List[ProjectListResponse])
def get_projects(
    request: Request,
    db: Session = Depends(get_db)
) -> List[ProjectListResponse]:
    """
    프로젝트 리스트 조회 API

    Args:
        request (Request): FastAPI의 Request 객체
        db (Session): SQLAlchemy 데이터베이스 세션

    Returns:
        List[ProjectListResponse]: 조회된 프로젝트 리스트
    """
    token_info = request.state.token_info
    user_id: int = token_info.get("userId")
    user_type: int = token_info.get("userType")
    if user_id is None or user_type is None:
        raise HTTPException(
            status_code=ERROR_MESSAGES["UNAUTHORIZED"]["status"],
            detail=ERROR_MESSAGES["UNAUTHORIZED"]["message"]
        )

    try:
        # 기업
        if user_type == 1:
            return ProjectService.get_projects(db)
        # 프리랜서
        else:
            return ProjectService.get_project_matchings(user_id, db)

    except HTTPException as e:
        raise e


@project.get("/{projectId}", response_model=ProjectDetailResponse)
def get_project_detail(
    project_id: int = Path(..., alias="projectId"),
    db: Session = Depends(get_db)
) -> ProjectDetailResponse:
    """
    프로젝트 상세 조회 API

    Args:
        request (Request): FastAPI의 Request 객체
        project_id (int): 프로젝트 ID
        db (Session): SQLAlchemy 데이터베이스 세션

    Returns:
        ProjectDetailResponse: 조회된 프로젝트 정보
    """
    try:
        return ProjectService.get_project_detail(project_id=project_id, db=db)
    except HTTPException as e:
        raise e


@project.get("/{projectId}/similar", response_model=List[ProjectListResponse])
def get_project_similar(
    project_id: int = Path(..., alias="projectId"),
    category_id: int = Query(..., alias="categoryId"),
    budget: int = Query(..., alias="budget"),
    db: Session = Depends(get_db)
) -> List[ProjectListResponse]:
    """
    유사한 프로젝트 리스트 조회 API

    Args:
        project_id (int): 프로젝트 ID
        category_id (int): 카테고리 ID
        budget (int): 금액
        db (Session): SQLAlchemy 데이터베이스 세션

    Returns:
        List[ProjectListResponse]: 조회된 프로젝트 리스트
    """
    try:
        return ProjectService.get_project_similar(project_id, category_id, budget, db)
    except HTTPException as e:
        raise e


@project.patch("/{projectId}/apply")
def update_project_apply(
    request: Request,
    project_id: int = Path(..., alias="projectId"),
    db: Session = Depends(get_db)
):
    """
    프로젝트 참여 지원 API

    Args:
        request (Request): FastAPI의 Request 객체
        project_id (int): 프로젝트 ID
        db (Session): SQLAlchemy 데이터베이스 세션
    """
    token_info = request.state.token_info
    user_id: int = token_info.get("userId")
    user_type: int = token_info.get("userType")
    if user_id is None or user_type is None:
        raise HTTPException(
            status_code=ERROR_MESSAGES["UNAUTHORIZED"]["status"],
            detail=ERROR_MESSAGES["UNAUTHORIZED"]["message"]
        )

    if user_type != 0:
        raise HTTPException(status_code=ERROR_MESSAGES["FORBIDDEN"]["status"],
                            detail=ERROR_MESSAGES["FORBIDDEN"]["message"])

    try:
        return ProjectService.update_project_apply(project_id, user_id, db)
    except HTTPException as e:
        raise e
