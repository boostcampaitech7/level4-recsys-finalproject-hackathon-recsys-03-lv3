from sqlalchemy.orm import Session
from src.models import Skill, Category, Location


class FilterService:
    def get_skills(db: Session) -> list:
        """
        모든 스킬 정보를 조회

        Args:
            db (Session): SQLAlchemy 세션 객체

        Returns:
            list: 스킬 정보 (skillId, skillName)를 포함하는 목록
        """
        skills = db.query(Skill.id.label("skillId"), Skill.name.label("skillName")).all()
        return [{"skillId": skill.skillId, "skillName": skill.skillName} for skill in skills] if skills else []

    def get_categories(db: Session) -> list:
        """
        모든 카테고리 정보를 조회

        Args:
            db (Session): SQLAlchemy 세션 객체

        Returns:
            list: 카테고리 정보 (categoryId, categoryName)를 포함하는 목록
        """
        categories = db.query(Category.id.label("categoryId"), Category.name.label("categoryName")).all()
        return [{"categoryId": category.categoryId, "categoryName": category.categoryName} for category in categories] if categories else []

    def get_locations(db: Session) -> list:
        """
        모든 지역 정보를 조회

        Args:
            db (Session): SQLAlchemy 세션 객체

        Returns:
            list: 지역 정보 (locationId, locationName)를 포함하는 목록
        """
        locations = db.query(Location.id.label("locationId"), Location.name.label("locationName")).all()
        return [{"locationId": location.locationId, "locationName": location.locationName} for location in locations] if locations else []
