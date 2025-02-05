from typing import List

from fastapi import APIRouter, Depends, Path, HTTPException, Request, BackgroundTasks
from sqlalchemy.orm import Session

from api.db import get_db
from src.schemas.project import ProjectRequest, FeedbackRequest, ProjectListResponse, ProjectFeedbackResponse, SolarResponse, CompanyResponse
from src.schemas.resource import ResourceListResponse
from src.services.project_service import ProjectService
from src.services.resource_service import ResourceService
from src.utils.user_handler import AuthRequired
from src.utils.error_messages import ERROR_MESSAGES

mymony = APIRouter(
    dependencies=[Depends(AuthRequired())]
)


@mymony.get("/applied-project", response_model=List[ProjectListResponse])
def get_applied_projects(
    request: Request,
    db: Session = Depends(get_db)
) -> List[ProjectListResponse]:
    """
    지원한 프로젝트 리스트 조회 API

    Args:
        request (Request): FastAPI의 Request 객체
        db (Session): SQLAlchemy 데이터베이스 세션

    Returns:
        List[ProjectListResponse]: 조회된 프로젝트 리스트
    """
    token_info = request.state.token_info
    user_id: int = token_info.get("userId")
    if user_id is None:
        raise HTTPException(
            status_code=ERROR_MESSAGES["UNAUTHORIZED"]["status"],
            detail=ERROR_MESSAGES["UNAUTHORIZED"]["message"]
        )

    try:
        return ProjectService.get_project_matchings(user_id, db, applied=1)
    except HTTPException as e:
        raise e


@mymony.get("/prestart-project", response_model=List[ProjectListResponse])
def get_prestart_projects(
    request: Request,
    db: Session = Depends(get_db)
) -> List[ProjectListResponse]:
    """
    등록한 프로젝트(시작 전) 리스트 조회 API

    Args:
        request (Request): FastAPI의 Request 객체
        db (Session): SQLAlchemy 데이터베이스 세션

    Returns:
        List[ProjectListResponse]: 조회된 프로젝트 리스트
    """
    token_info = request.state.token_info
    user_id: int = token_info.get("userId")
    if user_id is None:
        raise HTTPException(
            status_code=ERROR_MESSAGES["UNAUTHORIZED"]["status"],
            detail=ERROR_MESSAGES["UNAUTHORIZED"]["message"]
        )

    try:
        return ProjectService.get_projects(db, user_id=user_id, status=[0, 1])
    except HTTPException as e:
        raise e


@mymony.get("/prestart-project/{projectId}", response_model=List[ResourceListResponse])
def get_prestart_project_detail(
    project_id: int = Path(..., alias="projectId"),
    db: Session = Depends(get_db)
) -> List[ResourceListResponse]:
    """
    특정 프로젝트에 대한 추천 프리랜서 리스트 조회

    Args:
        project_id (int): 프로젝트 ID
        db (Session): SQLAlchemy 데이터베이스 세션

    Returns:
        List[ResourceListResponse]: 조회된 프리랜서 리스트
    """
    try:
        return ResourceService.get_resource_matchings(project_id, db)
    except HTTPException as e:
        raise e


@mymony.post("/project/init", response_model=SolarResponse)
def create_solar_response(
    request: Request,
    project_data: ProjectRequest,
    db: Session = Depends(get_db)
) -> SolarResponse:
    """
    프로젝트 등록 API
    새로운 프로젝트에 대한 정보를 입력하고 Solar를 호출해 응답을 반환한다.

    Args:
        request (Request): FastAPI의 Request 객체
        project_data (ProjectRequest): 프로젝트 내용, 기간, 예산 등을 포함하는 등록하려는 프로젝트 정보
        db (Session): SQLAlchemy 데이터베이스 세션

    Returns:
        SolarResponse: Solar 응답
    """
    token_info = request.state.token_info
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
        return ProjectService.create_solar_response(project_data, db)
    except HTTPException as e:
        raise e


@mymony.post("/project/register")
def create_project(
    request: Request,
    project_data: ProjectRequest,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = ...
) -> int:
    """
    프로젝트 등록 API
    새로운 프로젝트를 등록하고, 해당 프로젝트에 대한 매칭 정보를 저장한다.

    Args:
        request (Request): FastAPI의 Request 객체
        project_data (ProjectRequest): 프로젝트 기간, 내용 등을 포함한 요청 데이터
        db (Session): SQLAlchemy 데이터베이스 세션
        background_tasks (BackgroundTasks): 비동기 작업 실행을 위한 FastAPI 제공 도구

    Returns:
        int: 등록한 프로젝트 ID
    """
    token_info = request.state.token_info
    user_id: int = token_info.get("userId")
    if user_id is None:
        raise HTTPException(
            status_code=ERROR_MESSAGES["UNAUTHORIZED"]["status"],
            detail=ERROR_MESSAGES["UNAUTHORIZED"]["message"]
        )

    try:
        # 1. 프로젝트 등록
        project_id = ProjectService.create_project(user_id, project_data, db)

        # 2. 매칭정보 추론 및 저장 (비동기 실행)
        background_tasks.add_task(ProjectService.create_project_matching, project_id, db)

        return project_id
    except HTTPException as e:
        raise e


@mymony.get("/completed-project", response_model=List[ProjectFeedbackResponse])
def get_project_feedbacks(
    request: Request,
    db: Session = Depends(get_db)
) -> List[ProjectFeedbackResponse]:
    """
    등록한 프로젝트(완료) 리스트 조회 API

    Args:
        request (Request): FastAPI의 Request 객체
        db (Session): SQLAlchemy 데이터베이스 세션

    Returns:
        List[ProjectFeedbackResponse]: 조회된 프로젝트-피드백 리스트
    """
    token_info = request.state.token_info
    user_id: int = token_info.get("userId")
    if user_id is None:
        raise HTTPException(
            status_code=ERROR_MESSAGES["UNAUTHORIZED"]["status"],
            detail=ERROR_MESSAGES["UNAUTHORIZED"]["message"]
        )

    try:
        return ProjectService.get_project_feedbacks(db, user_id, search_type=1)
    except HTTPException as e:
        raise e


@mymony.post("/completed-project/feedback")
def create_project_feedback(
    request: Request,
    feedback_data: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """
    완료 프로젝트 피드백 등록 API

    Args:
        request (Request): FastAPI의 Request 객체
        feedback_data (FeedbackRequest): 피드백 점수, 내용 등을 포함한 요청 데이터
        db (Session): SQLAlchemy 데이터베이스 세션
    """
    token_info = request.state.token_info
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
        return ProjectService.create_project_feedback(feedback_data, db)
    except HTTPException as e:
        raise e


@mymony.get("/{companyId}/profile", response_model=CompanyResponse)
def get_company_profile(
    company_id: int = Path(..., alias="companyId"),
    db: Session = Depends(get_db)
) -> CompanyResponse:
    """
    기업 정보 조회 API

    Args:
        company_id (int): 기업 ID
        db (Session): SQLAlchemy 데이터베이스 세션

    Returns:
        CompanyResponse: 기업 정보
    """
    try:
        return ProjectService.get_company_profile(company_id, db)
    except HTTPException as e:
        raise e
