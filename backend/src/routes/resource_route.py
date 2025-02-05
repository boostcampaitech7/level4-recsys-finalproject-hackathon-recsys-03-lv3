from typing import List

from fastapi import APIRouter, Depends, Path, HTTPException, Request
from sqlalchemy.orm import Session

from api.db import get_db
from src.schemas.project import ProjectProgressResponse, ProjectListResponse, ProjectFeedbackResponse
from src.schemas.resource import ResourceListResponse
from src.services.project_service import ProjectService
from src.services.resource_service import ResourceService
from src.utils.user_handler import AuthRequired
from src.utils.error_messages import ERROR_MESSAGES

resource = APIRouter(
    dependencies=[Depends(AuthRequired())]
)


@resource.get("/")
def get_resources(db: Session = Depends(get_db)) -> List[ResourceListResponse]:
    """
    프리랜서 리스트 조회 API

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션

    Returns:
        List[ResourceListResponse]: 조회된 프리랜서 리스트
    """
    try:
        return ResourceService.get_resources(db)
    except HTTPException as e:
        raise e


@resource.get("/{freelancerId}/profile")
def get_resource_profile(
    freelancer_id: int = Path(..., alias="freelancerId"),
    db: Session = Depends(get_db)
) -> ResourceListResponse:
    """
    프리랜서 상세 조회(프로필) API

    Args:
        freelancer_id (int): 프리랜서 ID
        db (Session): SQLAlchemy 데이터베이스 세션

    Returns:
        ResourceListResponse: 조회된 프리랜서 정보
    """
    try:
        return ResourceService.get_resource_profile(freelancer_id, db)
    except HTTPException as e:
        return e


@resource.get("/{freelancerId}/progress")
def get_resource_progress(
    freelancer_id: int = Path(..., alias="freelancerId"),
    db: Session = Depends(get_db)
) -> ProjectProgressResponse:
    """
    프리랜서 상세 조회(프로젝트 진행상황) API

    Args:
        freelancer_id (int): 프리랜서 ID
        db (Session): SQLAlchemy 데이터베이스 세션

    Returns:
        ProjectProgressResponse: 조회된 프리랜서 진행상황 정보
    """
    try:
        return ProjectService.get_project_progress(freelancer_id, db)
    except HTTPException as e:
        return e


@resource.get("/{freelancerId}/feedback")
def get_resource_feedbacks(
    freelancer_id: int = Path(..., alias="freelancerId"),
    db: Session = Depends(get_db)
) -> List[ProjectFeedbackResponse]:
    """
    프리랜서의 프로젝트 조회 API

    Args:
        freelancer_id (int): 프리랜서 ID
        db (Session): SQLAlchemy 데이터베이스 세션

    Returns:
        List[ProjectFeedbackResponse]: 조회된 프로젝트-피드백 리스트
    """
    try:
        return ProjectService.get_project_feedbacks(db, user_id=freelancer_id, search_type=0)
    except HTTPException as e:
        raise e


@resource.get("/{freelancerId}/propose")
def get_resource_proposals(
    request: Request,
    freelancer_id: int = Path(..., alias="freelancerId"),
    db: Session = Depends(get_db)
) -> List[ProjectListResponse]:
    """
    제안할 프로젝트 리스트 조회 API

    Args:
        request (Request): FastAPI의 Request 객체
        freelancer_id (int): 프리랜서 ID
        db (Session): SQLAlchemy 데이터베이스 세션

    Returns:
        List[ProjectListResponse]: 조회된 프로젝트 리스트
    """
    token_info = request.state.token_info
    user_id: int = token_info.get("userId")
    user_type: int = token_info.get("userType")
    if user_type is None:
        raise HTTPException(
            status_code=ERROR_MESSAGES["UNAUTHORIZED"]["status"],
            detail=ERROR_MESSAGES["UNAUTHORIZED"]["message"]
        )

    if user_type != 1:
        raise HTTPException(status_code=ERROR_MESSAGES["FORBIDDEN"]["status"],
                            detail=ERROR_MESSAGES["FORBIDDEN"]["message"])

    try:
        return ProjectService.get_projects(db, user_id=user_id, status=[0])
    except HTTPException as e:
        raise e
