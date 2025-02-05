from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.db import get_db
from src.schemas.filter import Skill, Category, Location
from src.services.filter_service import FilterService

filter = APIRouter()


@filter.get("/skill", response_model=List[Skill])
def get_skills(db: Session = Depends(get_db)):
    """
    스킬 필터 API

    사용 가능한 모든 스킬 정보를 반환합니다.

    Args:
        db (Session): SQLAlchemy 세션 객체

    Returns:
        List[Skill]: 스킬 ID와 스킬 이름 목록
    """
    skills = FilterService.get_skills(db)
    if not skills:
        raise HTTPException(
            status_code=404,
            detail="요청한 리소스(스킬 정보)를 찾을 수 없습니다."
        )
    return skills


@filter.get("/category", response_model=List[Category])
def get_categories(db: Session = Depends(get_db)):
    """
    카테고리 필터 API

    사용 가능한 모든 카테고리 정보를 반환합니다.

    Args:
        db (Session): SQLAlchemy 세션 객체

    Returns:
        List[Category]: 카테고리 ID와 카테고리 이름 목록
    """
    categories = FilterService.get_categories(db)
    if not categories:
        raise HTTPException(
            status_code=404,
            detail="요청한 리소스(카테고리 정보)를 찾을 수 없습니다."
        )
    return categories


@filter.get("/location", response_model=List[Location])
def get_locations(db: Session = Depends(get_db)):
    """
    지역 필터 API

    사용 가능한 모든 지역 정보를 반환합니다.

    Args:
        db (Session): SQLAlchemy 세션 객체

    Returns:
        List[Location]: 지역 ID와 지역 이름 목록
    """
    locations = FilterService.get_locations(db)
    if not locations:
        raise HTTPException(
            status_code=404,
            detail="요청한 리소스(지역 정보)를 찾을 수 없습니다."
        )
    return locations