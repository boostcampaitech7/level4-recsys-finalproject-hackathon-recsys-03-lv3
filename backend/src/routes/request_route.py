from fastapi import APIRouter, Depends, Path, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from src.schemas.request import FeedbackResponse
from src.services.request_service import RequestService
from api.db import get_db
from src.utils.user_handler import AuthRequired
from src.utils.error_messages import ERROR_MESSAGES

request = APIRouter(
    dependencies=[Depends(AuthRequired())]
)


@request.get("/api/{root}/feedback", response_model=List[FeedbackResponse])
def get_feedback(
    request: Request,
    root: str = Path(...),
    db: Session = Depends(get_db)
) -> List[FeedbackResponse]:
    """
    메인(요청한 프로젝트) / 보낸 요청 조회 / 완료 프로젝트 조회 API

    Args:
        request (Request): FastAPI의 Request 객체
        root (str): 요청 페이지 구분 (main/request/receive)
        db (Session, optional): SQLAlchemy 데이터베이스 세션

    Returns:
        List[FeedbackResponse]: 조회된 요청 및 프로젝트 데이터 목록
    """
    try:
        token_info = request.state.token_info
        user_id: int = token_info.get("user_id")
        team_id: int = token_info.get("team_id")
    except Exception as e:
        raise HTTPException(status_code=ERROR_MESSAGES["UNAUTHORIZED"]["status"], detail=str(e))

    if root not in ["main", "request", "receive"]:
        raise HTTPException(status_code=ERROR_MESSAGES["BAD_REQUEST"]["status"],
                            detail=ERROR_MESSAGES["BAD_REQUEST"]["message"].format("경로"))

    try:
        return RequestService.get_feedback(root, user_id, team_id, db)
    except HTTPException as e:
        raise e
