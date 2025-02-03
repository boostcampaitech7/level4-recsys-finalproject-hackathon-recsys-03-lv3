from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import func, case, select, and_, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models import Project, Category, ProjectSkill, Skill, Company, Location, ProjectRanking, Feedback, FreelancerSkill
from src.schemas.project import ProjectRequest, FeedbackRequest, ProjectListResponse, ProjectDetailResponse, ProjectFeedbackResponse, CompanyResponse
from src.utils.error_messages import ERROR_MESSAGES

MAX_CNT = 50


class ProjectService:
    def get_projects(
        db: Session,
        user_id: Optional[int] = None,
        status: Optional[List[int]] = None,
        include_priority: Optional[bool] = None
    ) -> List[ProjectListResponse]:
        """
        프로젝트 리스트 조회 (기업)

        Args:
            db (Session): SQLAlchemy 데이터베이스 세션
            user_id (Optional[int]): 기업 ID
            status (Optional[int]): 진행 상태
            include_priority (Optional[bool]): 우선순위 포함 여부

        Returns:
            List[ProjectListResponse]: 조회된 프로젝트 리스트
        """
        query = (
            db.query(
                Project.id.label("projectId"),
                Project.name.label("projectName"),
                Project.duration.label("duration"),
                Project.budget.label("budget"),
                Project.work_type.label("workType"),
                Project.contract_type.label("contractType"),
                Project.status.label("status"),
                Project.register_date.label("registerDate"),
                Category.name.label("categoryName"),
                func.json_arrayagg(Skill.id).label("skillIdList"),
                func.json_arrayagg(Skill.name).label("skillNameList"),
                Location.name.label("locationName")
            )
        )

        if include_priority:
            query = query.add_columns(Project.priority.label("priority"))

        query = (
            query.join(Category, Project.category_id == Category.id)
                 .join(ProjectSkill, Project.id == ProjectSkill.project_id)
                 .join(Skill, ProjectSkill.skill_id == Skill.id)
                 .join(Company, Project.company_id == Company.id)
                 .join(Location, Company.location_id == Location.id)
        )

        if user_id is not None:
            query = query.filter(Project.company_id == user_id)

        if status is not None:
            query = query.filter(Project.status.in_(status))

        projects = (
            query.group_by(
                Project.id,
                Project.name,
                Project.duration,
                Project.budget,
                Project.work_type,
                Project.contract_type,
                Project.status,
                Project.register_date,
                Category.name,
                Location.name
            )
            .order_by(Project.register_date.desc())
            .limit(MAX_CNT)
            .all()
        )

        if not projects:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format("프로젝트 리스트")
            )

        return [ProjectListResponse(**dict(project._mapping)) for project in projects]

    def get_project_matchings(
        user_id: int,
        db: Session,
        applied: Optional[int] = None
    ) -> List[ProjectListResponse]:
        """
        프로젝트 리스트 조회 (프리랜서)

        Args:
            userId (int): 사용자 ID (프리랜서 또는 기업 ID)
            db (Session): SQLAlchemy 데이터베이스 세션
            applied (Optional[int]): 지원 여부

        Returns:
            List[ProjectListResponse]: 조회된 프로젝트 리스트
        """
        query = (
            db.query(
                Project.id.label("projectId"),
                Project.name.label("projectName"),
                Project.duration.label("duration"),
                Project.budget.label("budget"),
                Project.work_type.label("workType"),
                Project.contract_type.label("contractType"),
                Project.status.label("status"),
                Project.register_date.label("registerDate"),
                Category.name.label("categoryName"),
                func.json_arrayagg(Skill.id).label("skillIdList"),
                func.json_arrayagg(Skill.name).label("skillNameList"),
                Location.name.label("locationName"),
                ProjectRanking.matching_score.label("matchingScore"),
                ProjectRanking.applied.label("applied")
            )
            .join(Category, Project.category_id == Category.id)
            .join(ProjectSkill, Project.id == ProjectSkill.project_id)
            .join(Skill, ProjectSkill.skill_id == Skill.id)
            .join(Company, Project.company_id == Company.id)
            .join(Location, Company.location_id == Location.id)
            .outerjoin(ProjectRanking, and_(Project.id == ProjectRanking.project_id, ProjectRanking.freelancer_id == user_id))
        )

        if applied:
            query = query.filter(ProjectRanking.applied == 1)

        projects = (
            query.group_by(
                Project.id,
                Project.name,
                Project.duration,
                Project.budget,
                Project.work_type,
                Project.contract_type,
                Project.status,
                Project.register_date,
                Category.name,
                Location.name,
                ProjectRanking.matching_score,
                ProjectRanking.applied
            )
            .order_by(Project.register_date.desc())
            .limit(MAX_CNT)
            .all()
        )

        if not projects:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format("프로젝트 리스트")
            )

        return [ProjectListResponse(**dict(project._mapping)) for project in projects]

    def get_project_detail(project_id: int, db: Session) -> ProjectDetailResponse:
        """
        프로젝트 상세 조회

        Args:
            project_id (int): 프로젝트 ID
            db (Session): SQLAlchemy 데이터베이스 세션

        Returns:
            ProjectDetailResponse: 조회된 프로젝트 정보
        """
        project = (
            db.query(
                Project.id.label("projectId"),
                Project.name.label("projectName"),
                Project.duration.label("duration"),
                Project.budget.label("budget"),
                Project.work_type.label("workType"),
                Project.contract_type.label("contractType"),
                Project.priority.label("priority"),
                Project.status.label("status"),
                Project.register_date.label("registerDate"),
                Project.category_id.label("categoryId"),
                Category.name.label("categoryName"),
                func.json_arrayagg(Skill.name).label("skillList"),
                Project.company_id.label("companyId"),
                Company.name.label("companyName"),
                Location.name.label("locationName"),
            )
            .join(Category, Project.category_id == Category.id)
            .join(ProjectSkill, Project.id == ProjectSkill.project_id)
            .join(Skill, ProjectSkill.skill_id == Skill.id)
            .join(Company, Project.company_id == Company.id)
            .join(Location, Company.location_id == Location.id)
            .filter(Project.id == project_id)
            .group_by(
                Project.id,
                Project.name,
                Project.duration,
                Project.budget,
                Project.work_type,
                Project.contract_type,
                Project.priority,
                Project.status,
                Project.register_date,
                Project.category_id,
                Category.name,
                Project.company_id,
                Company.name,
                Location.name
            )
            .first()
        )

        if not project:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format(f"프로젝트 정보({project_id})")
            )

        project_content = (
            db.query(Project.content)
            .filter(Project.id == project_id)
            .scalar()
        )

        if project_content is not None:
            project_content = project_content.replace("\\n", "\n")

        project_dict = dict(project._mapping)
        project_dict["projectContent"] = project_content

        return ProjectDetailResponse(**project_dict)

    def get_project_similar(
        project_id: int,
        category_id: int,
        budget: int,
        db: Session
    ) -> List[ProjectListResponse]:
        """
        유사한 프로젝트 리스트 조회

        Args:
            project_id (int): 프로젝트 ID
            category_id (int): 카테고리 ID
            budget (int): 금액
            db (Session): SQLAlchemy 데이터베이스 세션

        Returns:
            List[ProjectListResponse]: 유사한 프로젝트 리스트
        """
        # 현재 프로젝트의 스킬 ID들을 가져오는 서브쿼리
        project_skills_agg_cte = (
            db.query(
                ProjectSkill.project_id.label("project_id"),
                func.json_arrayagg(Skill.id).label("skillIdList"),
                func.json_arrayagg(Skill.name).label("skillNameList")
            )
            .join(Skill, ProjectSkill.skill_id == Skill.id)
            .group_by(ProjectSkill.project_id)
        ).cte("project_skills_agg_cte")

        # 각 프로젝트별로 현재 프로젝트의 스킬과 일치하는 스킬 수를 미리 집계하는 서브쿼리
        matching_skill_count_cte = (
            db.query(
                ProjectSkill.project_id.label("project_id"),
                func.count().label("match_count")
            )
            .filter(
                ProjectSkill.skill_id.in_(
                    select(ProjectSkill.skill_id).where(ProjectSkill.project_id == project_id)
                )
            )
            .group_by(ProjectSkill.project_id)
        ).cte("matching_skill_count_cte")

        # 유사도 점수 계산
        similarity_expr = (
            case((Project.category_id == category_id, 5), else_=0)  # 카테고리 일치: 5점
            + (func.coalesce(matching_skill_count_cte.c.match_count, 0) * 3)  # 스킬 일치: 3점씩
            + case(
                (func.abs(Project.budget - budget) <= 100000, 2),
                (func.abs(Project.budget - budget) <= 500000, 1),
                else_=0,
            )  # 예산 차이: 100,000 이하 2점, 500,000 이하 1점, 그 외 0점
        ).label("similarityScore")

        projects = (
            db.query(
                Project.id.label("projectId"),
                Project.name.label("projectName"),
                Project.duration.label("duration"),
                Project.budget.label("budget"),
                Project.work_type.label("workType"),
                Project.contract_type.label("contractType"),
                Project.status.label("status"),
                Project.register_date.label("registerDate"),
                Category.name.label("categoryName"),
                project_skills_agg_cte.c.skillIdList,
                project_skills_agg_cte.c.skillNameList,
                Location.name.label("locationName"),
                similarity_expr,
            )
            .join(Category, Project.category_id == Category.id)
            .join(Company, Project.company_id == Company.id)
            .join(Location, Company.location_id == Location.id)
            .outerjoin(project_skills_agg_cte, project_skills_agg_cte.c.project_id == Project.id)
            .outerjoin(matching_skill_count_cte, matching_skill_count_cte.c.project_id == Project.id)
            .filter(Project.id != project_id)  # 현재 프로젝트 제외
            .order_by(
                similarity_expr.desc(),          # 유사도 점수 내림차순
                Project.register_date.desc(),      # 등록일 내림차순
            )
            .limit(6)
            .all()
        )

        if not projects:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format("유사한 프로젝트 리스트")
            )

        return [ProjectListResponse(**dict(project._mapping)) for project in projects]

    def update_project_apply(
        project_id: int,
        user_id: int,
        db: Session
    ):
        """
        프로젝트 참여 지원

        Args:
            project_id (int): 프로젝트 ID
            user_id (int): 프리랜서 ID
            db (Session): SQLAlchemy 데이터베이스 세션
        """
        # 프로젝트 지원 여부 확인
        project_ranking = (
            db.query(ProjectRanking)
            .filter(ProjectRanking.project_id == project_id)
            .filter(ProjectRanking.freelancer_id == user_id)
            .first()
        )

        if not project_ranking:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format("프로젝트 매칭 정보")
            )

        if project_ranking.applied == 1:
            raise HTTPException(
                status_code=ERROR_MESSAGES["CONFLICT"]["status"],
                detail=ERROR_MESSAGES["CONFLICT"]["message"].format("이미 지원한 프로젝트 입니다.")
            )

        try:
            project_ranking.applied = 1
            db.commit()
        except Exception:
            db.rollback()

    def create_project(
        user_id: int,
        project_data: ProjectRequest,
        db: Session
    ) -> int:
        """
        프로젝트 등록

        Args:
            user_id (int): 기업 ID
            project_data (ProjectRequest): 프로젝트 기간, 내용 등을 포함한 요청 데이터
            db (Session): SQLAlchemy 데이터베이스 세션

        Returns:
            int: 등록한 프로젝트 ID
        """
        try:
            # PROJECT
            new_project = Project(
                name=project_data.projectName,
                duration=project_data.duration,
                budget=project_data.budget,
                work_type=project_data.workType,
                contract_type=project_data.contractType,
                priority=project_data.priority,
                content=project_data.projectContent,
                status=0,
                register_date=project_data.registerDate,
                category_id=project_data.categoryId,
                company_id=user_id
            )

            db.add(new_project)
            db.flush(new_project)  # PROJECT_ID 가져오기

            # PROJECT_SKILL
            project_skills = [
                ProjectSkill(project_id=new_project.id, skill_id=skill_id)
                for skill_id in project_data.skillList
            ]
            db.add_all(project_skills)

            db.commit()
            return new_project.id  # 생성된 프로젝트 ID 반환

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=ERROR_MESSAGES["CONFLICT"]["status"],
                detail=ERROR_MESSAGES["CONFLICT"]["message"].format("이미 존재하는 프로젝트입니다.")
            )

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=ERROR_MESSAGES["UNPROCESSABLE_ENTITY"]["status"],
                detail=ERROR_MESSAGES["UNPROCESSABLE_ENTITY"]["message"].format(str(e))
            )

    def create_project_matching(
        project_id: int,
        db: Session
    ):
        pass

    def get_project_feedbacks(
        db: Session,
        user_id: int,
        search_type: int
    ) -> List[ProjectFeedbackResponse]:
        """
        등록한 프로젝트(완료) 리스트 조회

        Args:
            db (Session): SQLAlchemy 데이터베이스 세션
            user_id (int): 기업 ID
            search_type (int): 조회 조건 (0: 프리랜서, 1: 기업)

        Returns:
            List[ProjectFeedbackResponse]: 조회된 프로젝트-피드백 리스트
        """
        query = (
            db.query(
                Project.id.label("projectId"),
                Project.name.label("projectName"),
                Project.duration.label("duration"),
                Project.budget.label("budget"),
                Project.work_type.label("workType"),
                Project.contract_type.label("contractType"),
                Project.status.label("status"),
                Project.register_date.label("registerDate"),
                Category.name.label("categoryName"),
                Company.name.label("companyName"),
                func.json_arrayagg(Skill.id).label("skillIdList"),
                func.json_arrayagg(Skill.name).label("skillNameList"),
                func.round(
                    (func.coalesce(Feedback.expertise, 0)
                     + func.coalesce(Feedback.proactiveness, 0)
                     + func.coalesce(Feedback.punctuality, 0)
                     + func.coalesce(Feedback.communication, 0)
                     + func.coalesce(Feedback.maintainability, 0)) / 5, 1
                ).label("feedbackScore"),
                func.round(func.avg(Feedback.expertise), 1).label("expertise"),
                func.round(func.avg(Feedback.proactiveness), 1).label("proactiveness"),
                func.round(func.avg(Feedback.punctuality), 1).label("punctuality"),
                func.round(func.avg(Feedback.communication), 1).label("communication"),
                func.round(func.avg(Feedback.maintainability), 1).label("maintainability"),
                Feedback.content.label("feedbackContent")
            )
            .join(Category, Project.category_id == Category.id)
            .join(Company, Project.company_id == Company.id)
            .join(ProjectSkill, Project.id == ProjectSkill.project_id)
            .join(Skill, ProjectSkill.skill_id == Skill.id)
            .outerjoin(Feedback, Project.id == Feedback.project_id)
        )

        error_message = ""
        # 프리랜서
        if search_type == 0:
            query = query.filter(Project.freelancer_id == user_id, Project.status.in_(1, 2))
            error_message = f"프리랜서({user_id})의 프로젝트 리스트"
        # 기업
        elif search_type == 1:
            query = query.filter(Project.company_id == user_id, Project.status == 2)
            error_message = "완료한 프로젝트 리스트"

        projects = (
            query.group_by(
                Project.id,
                Project.name,
                Project.duration,
                Project.budget,
                Project.work_type,
                Project.contract_type,
                Project.status,
                Project.register_date,
                Category.name,
                Company.name,
                Feedback.content
            )
            .order_by(Project.register_date.desc())
            .limit(MAX_CNT)
            .all()
        )

        if not projects:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format(error_message)
            )

    def create_project_feedback(
        feedback_data: FeedbackRequest,
        db: Session
    ):
        """
        완료 프로젝트 피드백 등록

        Args:
            feedback_data (FeedbackRequest): 피드백 점수, 내용 등을 포함한 요청 데이터
            db (Session): SQLAlchemy 데이터베이스 세션
        """
        try:
            # FEEDBACK
            new_feedback = Feedback(
                expertise=feedback_data.expertise,
                proactiveness=feedback_data.proactiveness,
                punctuality=feedback_data.punctuality,
                communication=feedback_data.communication,
                maintainability=feedback_data.maintainability,
                content=feedback_data.feedbackContent,
                project_id=feedback_data.projectId,
                freelancer_id=feedback_data.freelancerId
            )

            db.add(new_feedback)

            # FREELANCER_SKILL의 SKILL_SCORE 수정
            for skill_id in feedback_data.skillList:
                db.execute(
                    update(FreelancerSkill)
                    .where(
                        FreelancerSkill.freelancer_id == feedback_data.freelancerId,
                        FreelancerSkill.skill_id == skill_id
                    )
                    .values(skill_score=(FreelancerSkill.skill_score * 0.8 + feedback_data.expertise * 0.2))
                )

            db.commit()

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=ERROR_MESSAGES["CONFLICT"]["status"],
                detail=ERROR_MESSAGES["CONFLICT"]["message"].format("이미 존재하는 피드백입니다.")
            )

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=ERROR_MESSAGES["UNPROCESSABLE_ENTITY"]["status"],
                detail=ERROR_MESSAGES["UNPROCESSABLE_ENTITY"]["message"].format(str(e))
            )

    def get_company_profile(
        company_id: int,
        db: Session
    ) -> CompanyResponse:
        """
        기업 정보 조회

        Args:
            company_id (int): 기업 ID
            db (Session): SQLAlchemy 데이터베이스 세션

        Returns:
            CompanyResponse: 조회된 기업 정보
        """
        company = (
            db.query(
                Company.id.label("companyId"),
                Company.name.label("companyName"),
                Company.content.label("companyContent"),
                Location.name.label("locationName")
            )
            .join(Location, Company.location_id == Location.id)
            .filter(Company.id == company_id)
            .first()
        )

        if not company:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format(f"기업 정보({company_id})")
            )

        return CompanyResponse(**dict(company))
