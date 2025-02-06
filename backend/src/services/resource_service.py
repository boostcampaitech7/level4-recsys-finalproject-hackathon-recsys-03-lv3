from typing import List

from fastapi import HTTPException
from sqlalchemy import func, and_, case
from sqlalchemy.orm import Session

from src.models import Freelancer, Category, Location, Skill, FreelancerSkill, Feedback, ProjectRanking, ProjectApplicants, FreelancerCategory
from src.schemas.resource import ResourceListResponse
from src.utils.error_messages import ERROR_MESSAGES

MAX_CNT = 50


class ResourceService:
    def get_resources(db: Session) -> List[ResourceListResponse]:
        """
        프리랜서 리스트 조회

        Args:
            db (Session): SQLAlchemy 데이터베이스 세션

        Returns:
            List[ResourceListResponse]: 조회된 프리랜서 리스트
        """
        category_sub = (
            db.query(
                FreelancerCategory.freelancer_id.label("freelancer_id"),
                func.json_arrayagg(Category.name).label("category_list")
            )
            .join(Category, FreelancerCategory.category_id == Category.id)
            .group_by(FreelancerCategory.freelancer_id)
            .subquery()
        )

        skill_sub = (
            db.query(
                FreelancerSkill.freelancer_id.label("freelancer_id"),
                func.json_arrayagg(Skill.name).label("skill_list"),
                func.json_arrayagg(FreelancerSkill.skill_score).label("skill_score_list")
            )
            .join(Skill, FreelancerSkill.skill_id == Skill.id)
            .group_by(FreelancerSkill.freelancer_id)
            .subquery()
        )

        feedback_sub = (
            db.query(
                Feedback.freelancer_id.label("freelancer_id"),
                func.count(Feedback.id).label("feedbackCount"),
                func.round(
                    func.avg(
                        func.coalesce(Feedback.expertise, 0)
                        + func.coalesce(Feedback.proactiveness, 0)
                        + func.coalesce(Feedback.punctuality, 0)
                        + func.coalesce(Feedback.communication, 0)
                        + func.coalesce(Feedback.maintainability, 0)
                    ) / 5, 1
                ).label("feedbackScore"),
                func.round(func.avg(Feedback.expertise), 1).label("expertise"),
                func.round(func.avg(Feedback.proactiveness), 1).label("proactiveness"),
                func.round(func.avg(Feedback.punctuality), 1).label("punctuality"),
                func.round(func.avg(Feedback.communication), 1).label("communication"),
                func.round(func.avg(Feedback.maintainability), 1).label("maintainability")
            )
            .group_by(Feedback.freelancer_id)
            .subquery()
        )

        resources = (
            db.query(
                Freelancer.id.label("freelancerId"),
                Freelancer.name.label("freelancerName"),
                Freelancer.work_exp.label("workExp"),
                Freelancer.work_type.label("workType"),
                Freelancer.role.label("role"),
                Location.name.label("locationName"),
                category_sub.c.category_list.label("categoryList"),
                skill_sub.c.skill_list.label("skillList"),
                skill_sub.c.skill_score_list.label("skillScoreList"),
                feedback_sub.c.feedbackCount.label("feedbackCount"),
                feedback_sub.c.feedbackScore.label("feedbackScore"),
                feedback_sub.c.expertise.label("expertise"),
                feedback_sub.c.proactiveness.label("proactiveness"),
                feedback_sub.c.punctuality.label("punctuality"),
                feedback_sub.c.communication.label("communication"),
                feedback_sub.c.maintainability.label("maintainability")
            )
            .join(Location, Freelancer.location_id == Location.id)
            .join(category_sub, category_sub.c.freelancer_id == Freelancer.id)
            .join(skill_sub, skill_sub.c.freelancer_id == Freelancer.id)
            .outerjoin(feedback_sub, feedback_sub.c.freelancer_id == Freelancer.id)
            .filter(feedback_sub.c.feedbackScore.isnot(None))
            .order_by(Freelancer.id.desc())
            .limit(MAX_CNT)
            .all()
        )

        if not resources:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format("프리랜서 리스트")
            )

        freelancer_ids = [row._mapping["freelancerId"] for row in resources]
        content_rows = (
            db.query(Freelancer.id, Freelancer.content)
            .filter(Freelancer.id.in_(freelancer_ids))
            .all()
        )
        content_dict = {row.id: row.content for row in content_rows}

        resource_results = []
        for row in resources:
            result_dict = dict(row._mapping)
            fc = content_dict.get(result_dict["freelancerId"])
            # LOB 객체인 경우 문자열로 변환
            if fc is not None and hasattr(fc, "read"):
                result_dict["freelancerContent"] = fc.read()
            else:
                result_dict["freelancerContent"] = fc
            resource_results.append(ResourceListResponse(**result_dict))

        return resource_results

    def get_resource_profile(
        freelancer_id: int,
        db: Session
    ) -> ResourceListResponse:
        """
        프리랜서 상세 조회(프로필)

        Args:
            freelancer_id (int): 프리랜서 ID
            db (Session): SQLAlchemy 데이터베이스 세션

        Returns:
            ResourceListResponse: 조회된 프리랜서 정보
        """
        category_sub = (
            db.query(
                FreelancerCategory.freelancer_id.label("freelancer_id"),
                func.json_arrayagg(Category.name).label("category_list")
            )
            .join(Category, FreelancerCategory.category_id == Category.id)
            .group_by(FreelancerCategory.freelancer_id)
            .subquery()
        )

        skill_sub = (
            db.query(
                FreelancerSkill.freelancer_id.label("freelancer_id"),
                func.json_arrayagg(Skill.name).label("skill_list"),
                func.json_arrayagg(FreelancerSkill.skill_score).label("skill_score_list")
            )
            .join(Skill, FreelancerSkill.skill_id == Skill.id)
            .group_by(FreelancerSkill.freelancer_id)
            .subquery()
        )

        feedback_sub = (
            db.query(
                Feedback.freelancer_id.label("freelancer_id"),
                func.count(Feedback.id).label("feedbackCount"),
                func.round(
                    func.avg(
                        func.coalesce(Feedback.expertise, 0)
                        + func.coalesce(Feedback.proactiveness, 0)
                        + func.coalesce(Feedback.punctuality, 0)
                        + func.coalesce(Feedback.communication, 0)
                        + func.coalesce(Feedback.maintainability, 0)
                    ) / 5, 1
                ).label("feedbackScore"),
                func.round(func.avg(Feedback.expertise), 1).label("expertise"),
                func.round(func.avg(Feedback.proactiveness), 1).label("proactiveness"),
                func.round(func.avg(Feedback.punctuality), 1).label("punctuality"),
                func.round(func.avg(Feedback.communication), 1).label("communication"),
                func.round(func.avg(Feedback.maintainability), 1).label("maintainability")
            )
            .group_by(Feedback.freelancer_id)
            .subquery()
        )

        resource = (
            db.query(
                Freelancer.id.label("freelancerId"),
                Freelancer.name.label("freelancerName"),
                Freelancer.work_exp.label("workExp"),
                Freelancer.price.label("price"),
                Freelancer.work_type.label("workType"),
                Freelancer.role.label("role"),
                Location.name.label("locationName"),
                category_sub.c.category_list.label("categoryList"),
                skill_sub.c.skill_list.label("skillList"),
                skill_sub.c.skill_score_list.label("skillScoreList"),
                feedback_sub.c.feedbackCount.label("feedbackCount"),
                feedback_sub.c.feedbackScore.label("feedbackScore"),
                feedback_sub.c.expertise.label("expertise"),
                feedback_sub.c.proactiveness.label("proactiveness"),
                feedback_sub.c.punctuality.label("punctuality"),
                feedback_sub.c.communication.label("communication"),
                feedback_sub.c.maintainability.label("maintainability")
            )
            .join(Location, Freelancer.location_id == Location.id)
            .join(category_sub, category_sub.c.freelancer_id == Freelancer.id)
            .join(skill_sub, skill_sub.c.freelancer_id == Freelancer.id)
            .outerjoin(feedback_sub, feedback_sub.c.freelancer_id == Freelancer.id)
            .filter(Freelancer.id == freelancer_id)
            .first()
        )

        if not resource:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format(f"프리랜서({freelancer_id}) 정보")
            )

        resource_content = (
            db.query(Freelancer.content)
            .filter(Freelancer.id == freelancer_id)
            .scalar()
        )

        if resource_content is not None:
            resource_content = resource_content.replace("\\n", "\n")

        resource_dict = dict(resource._mapping)
        resource_dict["freelancerContent"] = resource_content

        return ResourceListResponse(**resource_dict)

    def get_resource_matchings(
        project_id: int,
        db: Session
    ) -> List[ResourceListResponse]:
        """
        특정 프로젝트에 대한 추천 프리랜서 리스트 조회

        Args:
            project_id (int): 프로젝트 ID
            db (Session): SQLAlchemy 데이터베이스 세션

        Returns:
            List[ResourceListResponse]: 조회된 프리랜서 리스트
        """
        category_sub = (
            db.query(
                FreelancerCategory.freelancer_id.label("freelancer_id"),
                func.json_arrayagg(Category.name).label("category_list")
            )
            .join(Category, FreelancerCategory.category_id == Category.id)
            .group_by(FreelancerCategory.freelancer_id)
            .subquery()
        )

        skill_sub = (
            db.query(
                FreelancerSkill.freelancer_id.label("freelancer_id"),
                func.json_arrayagg(Skill.name).label("skill_list"),
                func.json_arrayagg(FreelancerSkill.skill_score).label("skill_score_list")
            )
            .join(Skill, FreelancerSkill.skill_id == Skill.id)
            .group_by(FreelancerSkill.freelancer_id)
            .subquery()
        )

        feedback_sub = (
            db.query(
                Feedback.freelancer_id.label("freelancer_id"),
                Feedback.project_id.label("project_id"),
                func.count(Feedback.id).label("feedbackCount"),
                func.round(
                    func.avg(
                        func.coalesce(Feedback.expertise, 0)
                        + func.coalesce(Feedback.proactiveness, 0)
                        + func.coalesce(Feedback.punctuality, 0)
                        + func.coalesce(Feedback.communication, 0)
                        + func.coalesce(Feedback.maintainability, 0)
                    ) / 5, 1
                ).label("feedbackScore"),
                func.round(func.avg(Feedback.expertise), 1).label("expertise"),
                func.round(func.avg(Feedback.proactiveness), 1).label("proactiveness"),
                func.round(func.avg(Feedback.punctuality), 1).label("punctuality"),
                func.round(func.avg(Feedback.communication), 1).label("communication"),
                func.round(func.avg(Feedback.maintainability), 1).label("maintainability")
            )
            .group_by(
                Feedback.freelancer_id,
                Feedback.project_id
            )
            .subquery()
        )

        resources = (
            db.query(
                Freelancer.id.label("freelancerId"),
                Freelancer.name.label("freelancerName"),
                Freelancer.work_exp.label("workExp"),
                Freelancer.work_type.label("workType"),
                Freelancer.role.label("role"),
                Location.name.label("locationName"),
                category_sub.c.category_list.label("categoryList"),
                skill_sub.c.skill_list.label("skillList"),
                skill_sub.c.skill_score_list.label("skillScoreList"),
                feedback_sub.c.feedbackCount.label("feedbackCount"),
                feedback_sub.c.feedbackScore.label("feedbackScore"),
                feedback_sub.c.expertise.label("expertise"),
                feedback_sub.c.proactiveness.label("proactiveness"),
                feedback_sub.c.punctuality.label("punctuality"),
                feedback_sub.c.communication.label("communication"),
                feedback_sub.c.maintainability.label("maintainability"),
                ProjectRanking.matching_score.label("matchingScore"),
                case(
                    (ProjectApplicants.freelancer_id.isnot(None), 1),
                    else_=0
                ).label("applied")
            )
            .join(Location, Freelancer.location_id == Location.id)
            .join(ProjectRanking, and_(
                ProjectRanking.project_id == project_id,
                Freelancer.id == ProjectRanking.freelancer_id
            ))
            .join(category_sub, category_sub.c.freelancer_id == Freelancer.id)
            .join(skill_sub, skill_sub.c.freelancer_id == Freelancer.id)
            .outerjoin(feedback_sub, and_(
                feedback_sub.c.freelancer_id == Freelancer.id,
                feedback_sub.c.project_id == project_id))
            .outerjoin(ProjectApplicants, and_(
                Freelancer.id == ProjectApplicants.freelancer_id,
                ProjectApplicants.project_id == project_id
            ))
            .order_by(ProjectRanking.matching_score.desc())
            .limit(MAX_CNT)
            .all()
        )

        if not resources:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format(f"프로젝트({project_id})의 추천 프리랜서 리스트")
            )

        freelancer_ids = [row._mapping["freelancerId"] for row in resources]
        content_rows = (
            db.query(Freelancer.id, Freelancer.content)
            .filter(Freelancer.id.in_(freelancer_ids))
            .all()
        )
        content_dict = {row.id: row.content for row in content_rows}

        resource_results = []
        for row in resources:
            result_dict = dict(row._mapping)
            fc = content_dict.get(result_dict["freelancerId"])
            # LOB 객체인 경우 문자열로 변환
            if fc is not None and hasattr(fc, "read"):
                result_dict["freelancerContent"] = fc.read()
            else:
                result_dict["freelancerContent"] = fc
            resource_results.append(ResourceListResponse(**result_dict))

        return resource_results
