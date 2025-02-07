from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models import Skill, Category, Location
from src.schemas.filter import SkillResponse, CategoryResponse, LocationResponse
from src.utils.error_messages import ERROR_MESSAGES


class FilterService:
    def get_skills(db: Session) -> List[SkillResponse]:
        """
        모든 스킬 정보를 조회

        Args:
            db (Session): SQLAlchemy 세션 객체

        Returns:
            List[SkillResponse]: 스킬 정보 (skillId, skillName)를 포함하는 목록
        """
        skills = db.query(
            Skill.id.label("skillId"),
            Skill.name.label("skillName")
        ).all()

        if not skills:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format("스킬 정보")
            )

        return [SkillResponse(**dict(skill._mapping)) for skill in skills]

    def get_categories(db: Session) -> List[CategoryResponse]:
        """
        모든 카테고리 정보를 조회

        Args:
            db (Session): SQLAlchemy 세션 객체

        Returns:
            List[CategoryResponse]: 카테고리 정보 (categoryId, categoryName)를 포함하는 목록
        """
        categories = db.query(
            Category.id.label("categoryId"),
            Category.name.label("categoryName")
        ).all()

        if not categories:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format("도메인 정보")
            )

        return [CategoryResponse(**dict(category._mapping)) for category in categories]

    def get_locations(db: Session) -> List[LocationResponse]:
        """
        모든 지역 정보를 조회

        Args:
            db (Session): SQLAlchemy 세션 객체

        Returns:
            List[LocationResponse]: 지역 정보 (locationId, locationName)를 포함하는 목록
        """
        locations = db.query(
            Location.id.label("locationId"),
            Location.name.label("locationName")
        ).all()

        if not locations:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format("지역 정보")
            )

        return [LocationResponse(**dict(location._mapping)) for location in locations]
