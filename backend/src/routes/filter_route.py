from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.db import get_db
from src.services.filter_service import FilterService

filter = APIRouter()


@filter.get("/skill")
def get_skills(db: Session = Depends(get_db)):
    """
    스킬 필터 API

    사용 가능한 모든 스킬 정보를 반환

    Args:
        db (Session): SQLAlchemy 세션 객체

    Returns:
        list: 스킬 ID와 스킬 이름 목록
    """
    skills = FilterService.get_skills(db)
    if not skills:
        raise HTTPException(
            status_code=404,
            detail="요청한 리소스(스킬 정보)를 찾을 수 없습니다."
        )
    return [{"skillId": skill["skillId"], "skillName": skill["skillName"]} for skill in skills]


@filter.get("/category")
def get_categories(db: Session = Depends(get_db)):
    """
    카테고리 필터 API

    사용 가능한 모든 카테고리 정보를 반환

    Args:
        db (Session): SQLAlchemy 세션 객체

    Returns:
        list: 카테고리 ID와 카테고리 이름 목록
    """
    categories = FilterService.get_categories(db)
    if not categories:
        raise HTTPException(
            status_code=404,
            detail="요청한 리소스(카테고리 정보)를 찾을 수 없습니다."
        )
    return [{"categoryId": category["categoryId"], "categoryName": category["categoryName"]} for category in categories]


@filter.get("/location")
def get_locations(db: Session = Depends(get_db)):
    """
    지역 필터 API

    사용 가능한 모든 지역 정보를 반환

    Args:
        db (Session): SQLAlchemy 세션 객체

    Returns:
        list: 지역 ID와 지역 이름 목록
    """
    locations = FilterService.get_locations(db)
    if not locations:
        raise HTTPException(
            status_code=404,
            detail="요청한 리소스(지역 정보)를 찾을 수 없습니다."
        )
    return [{"locationId": location["locationId"], "locationName": location["locationName"]} for location in locations]
