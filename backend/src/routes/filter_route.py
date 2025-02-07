from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db import get_db
from src.schemas.filter import SkillResponse, CategoryResponse, LocationResponse
from src.services.filter_service import FilterService

filter = APIRouter()


@filter.get("/skill", response_model=List[SkillResponse])
def get_skills(db: Session = Depends(get_db)) -> List[SkillResponse]:
    """
    스킬 필터 API

    사용 가능한 모든 스킬 정보를 반환

    Args:
        db (Session): SQLAlchemy 세션 객체

    Returns:
        List[SkillResponse]: 스킬 ID와 스킬 이름 목록
    """
    try:
        return FilterService.get_skills(db)
    except HTTPException as e:
        raise e


@filter.get("/category", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)) -> List[CategoryResponse]:
    """
    카테고리 필터 API

    사용 가능한 모든 카테고리 정보를 반환

    Args:
        db (Session): SQLAlchemy 세션 객체

    Returns:
        List[CategoryResponse]: 카테고리 ID와 카테고리 이름 목록
    """
    try:
        return FilterService.get_categories(db)
    except HTTPException as e:
        raise e


@filter.get("/location", response_model=List[LocationResponse])
def get_locations(db: Session = Depends(get_db)) -> List[LocationResponse]:
    """
    지역 필터 API

    사용 가능한 모든 지역 정보를 반환

    Args:
        db (Session): SQLAlchemy 세션 객체

    Returns:
        List[LocationResponse]: 지역 ID와 지역 이름 목록
    """
    try:
        return FilterService.get_locations(db)
    except HTTPException as e:
        raise e
