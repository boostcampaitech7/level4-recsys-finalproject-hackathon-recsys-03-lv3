from fastapi import HTTPException
from sqlalchemy.orm import Session, aliased
from typing import List
from sqlalchemy import and_

from src.models import Project, Feedback, User, Team
from src.schemas.request import FeedbackResponse
from src.utils.error_messages import ERROR_MESSAGES


class RequestService:
    def get_feedback(
            root: str,
            user_id: int,
            team_id: int,
            db: Session
    ) -> List[FeedbackResponse]:
        """
        보낸 요청 및 완료 프로젝트 조회 기능

        Args:
            root (str): 요청 페이지 구분 (main/request/receive)
            user_id (int): 사용자 ID
            team_id (int): 팀 ID
            db (Session): SQLAlchemy 데이터베이스 세션

        Returns:
            List[FeedbackResponse]: 조회된 요청 및 프로젝트 데이터 목록
        """
        Manager = aliased(User)  # 팀장의 이름
        Requester = aliased(User)  # 요청자의 이름

        query = (
            db.query(
                Project.id.label("projectId"),
                Project.name.label("projectName"),
                Project.start_date.label("startDate"),
                Project.end_date.label("endDate"),
                Feedback.score.label("feedbackScore"),
                Manager.name.label("manageName"),  # 팀장의 이름
                Requester.name.label("requestName"),  # 요청자의 이름
                Project.progress_status.label("status")
            )
            .join(Team, Project.team_id == Team.id)
            .join(Manager, and_(Team.id == Manager.team_id, Manager.position_id == 1))
            .join(Requester, Project.user_id == Requester.id)
            .outerjoin(Feedback, Project.id == Feedback.project_id)
        )

        if root == "receive":
            query = query.filter(Project.progress_status == 3, Project.team_id == team_id)
        elif root in ["main", "request"]:
            query = query.filter(Project.user_id == user_id)

        results = query.all()

        if not results:
            raise HTTPException(status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format(""))

        return [FeedbackResponse(**result._asdict()) for result in results]
