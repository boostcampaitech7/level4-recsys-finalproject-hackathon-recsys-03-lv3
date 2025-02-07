import json
import pickle
import logging
import pandas as pd
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import func, case, select, and_, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage, HumanMessage

from api.upstage import chat_with_solar
from src.models import Project, Category, ProjectSkill, Skill, Company, Location, ProjectRanking, ProjectApplicants, Feedback, FreelancerSkill, Freelancer
from src.schemas.project import ProjectRequest, FeedbackRequest, ProjectListResponse, ProjectDetailResponse, ProjectFeedbackResponse, SolarResponse, CompanyResponse, ProjectProgressResponse
from src.services.filter_service import FilterService
from src.routes.websocket_route import notify_client
from src.utils.error_messages import ERROR_MESSAGES
from src.utils.utils import download_model_file

MAX_CNT = 50
logger = logging.getLogger(__name__)


class ProjectService:
    def get_projects(
        db: Session,
        user_id: Optional[int] = None,
        status: Optional[List[int]] = None
    ) -> List[ProjectListResponse]:
        """
        프로젝트 리스트 조회 (기업)

        Args:
            db (Session): SQLAlchemy 데이터베이스 세션
            user_id (Optional[int]): 기업 ID
            status (Optional[int]): 진행 상태

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
            .join(Category, Project.category_id == Category.id)
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
            .limit(MAX_CNT).all()
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
                case(
                    (Project.status == 0, ProjectRanking.matching_score),
                    else_=None
                ).label("matchingScore"),
                case(
                    (ProjectApplicants.freelancer_id.isnot(None), 1),
                    else_=0
                ).label("applied")
            )
            .join(Category, Project.category_id == Category.id)
            .join(ProjectSkill, Project.id == ProjectSkill.project_id)
            .join(Skill, ProjectSkill.skill_id == Skill.id)
            .join(Company, Project.company_id == Company.id)
            .join(Location, Company.location_id == Location.id)
            .outerjoin(ProjectRanking, and_(Project.id == ProjectRanking.project_id, ProjectRanking.freelancer_id == user_id))
            .outerjoin(ProjectApplicants, and_(Project.id == ProjectApplicants.project_id, ProjectApplicants.freelancer_id == user_id))
        )

        if applied:
            query = query.filter(ProjectApplicants.freelancer_id == user_id)

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
                Category.id,
                Category.name,
                Location.name,
                ProjectRanking.matching_score,
                ProjectApplicants.freelancer_id
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
        db: Session,
        skill_list: Optional[List[int]] = None
    ) -> List[ProjectListResponse]:
        """
        유사한 프로젝트 리스트 조회

        Args:
            project_id (int): 프로젝트 ID
            category_id (int): 카테고리 ID
            budget (int): 금액
            db (Session): SQLAlchemy 데이터베이스 세션
            skill_list(Optional[List[int]]): 스킬 ID 리스트

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
        if skill_list:
            limit_cnt = 50
            skill_filter = skill_list
        else:
            limit_cnt = 6
            skill_filter = select(ProjectSkill.skill_id).where(ProjectSkill.project_id == project_id)

        matching_skill_count_cte = (
            db.query(
                ProjectSkill.project_id.label("project_id"),
                func.count().label("match_count")
            )
            .filter(ProjectSkill.skill_id.in_(skill_filter))
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
                similarity_expr.desc(),  # 유사도 점수 내림차순
                Project.register_date.desc(),  # 등록일 내림차순
            )
            .limit(limit_cnt)
            .all()
        )

        if not projects:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format("유사한 프로젝트 리스트")
            )

        return [ProjectListResponse(**dict(project._mapping)) for project in projects]

    def create_project_apply(
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
            db.query(ProjectApplicants)
            .filter(ProjectApplicants.project_id == project_id)
            .filter(ProjectApplicants.freelancer_id == user_id)
            .first()
        )

        if project_ranking:
            raise HTTPException(
                status_code=ERROR_MESSAGES["CONFLICT"]["status"],
                detail=ERROR_MESSAGES["CONFLICT"]["message"].format("이미 지원한 프로젝트 입니다.")
            )

        try:
            new_project_applicant = ProjectApplicants(
                project_id=project_id,
                freelancer_id=user_id
            )
            db.add(new_project_applicant)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=ERROR_MESSAGES["UNPROCESSABLE_ENTITY"]["status"],
                detail=ERROR_MESSAGES["UNPROCESSABLE_ENTITY"]["message"].format(str(e))
            )

    def create_solar_response(
        project_data: ProjectRequest,
        db: Session
    ) -> SolarResponse:
        """
        Solar와 대화해 프로젝트 정보를 자동 생성

        Args:
            project_data (ProjectRequest): 프로젝트 내용, 기간, 예산 등을 포함하는 등록하려는 프로젝트 정보
            db (Session): SQLAlchemy 데이터베이스 세션

        Returns:
            dict: 변환된 프로젝트 데이터
        """
        try:
            skill_list = FilterService.get_skills(db)
            category_list = FilterService.get_categories(db)
        except HTTPException as e:
            raise e

        try:
            # 1. 대화 memory 생성
            memory = ConversationBufferMemory(return_messages=True)

            # 2. 설정 정보 생성
            system_message = "너의 이름은 HRmony야. 한글 데이터를 입력받고 한글로 답변해야 해. 기업이 프리랜서를 모집할 프로젝트 공고를 올릴 때 도움을 주는 AI야."
            memory.chat_memory.add_message(SystemMessage(content=system_message))

            # 3. 첫번째 대화: 프로젝트 정보 생성
            memory.chat_memory.add_message(HumanMessage(content="다음은 프로젝트 등록을 위한 카테고리 및 스킬 정보야."))
            category_info = json.dumps([category.__dict__ for category in category_list], ensure_ascii=False)
            skill_info = json.dumps([skill.__dict__ for skill in skill_list], ensure_ascii=False)
            memory.chat_memory.add_message(HumanMessage(content="카테고리 정보: " + category_info))
            memory.chat_memory.add_message(HumanMessage(content="스킬 정보: " + skill_info))

            chat_history = [msg.content for msg in memory.chat_memory.messages]
            project_info = json.dumps(project_data.dict(), ensure_ascii=False)
            memory.chat_memory.add_message(HumanMessage(content="새로운 프로젝트 등록 요청: " + project_info))
            new_project_instruction = """
            다음은 프로젝트 등록 정보야.
            이 정보들을 기반으로 projectName, categoryId, skillList, projectContent를 전달해줘.
            1) projectName은 projectContent를 요약하는 내용으로 넣어줘.
            2) categoryId는 프로젝트 내용을 보고 카테고리 목록 중 어떤 카테고리에 해당할 지 id값으로 넣어줘. id에 해당하는 categoryName도 넣어줘.
            3) skillId는 projectContent를 보고 어떤 스킬이 필요할 지 스킬 목록에서 찾아서 id값으로 넣어줘 (skillIdList). (최대 6개) projectContent에서 개발 언어가 나오는 경우 스킬정보에서 찾아줘. 예를 들어, mysql이라면 skillId 121, skillName MySQL으로 해줘. 해당하는 skillName도 넣어줘 (skillNameList)
            4) projectContent의 내용은 입력 받은 projectContent를 5)와 같이 형식에 맞추어서 요약해서 적어줘.
            5) projectContent의 내용 형식은 <프로젝트 진행 방식>, <프로젝트의 현재 상황>, <상세한 업무 내용>, <참고 자료 / 유의 사항> 영역으로 나누어서 적어줘. 말투는 '~ 입니다.' 존댓말로 정리해줘. '개행기호'을 포함해서 적어줘. (projectContent 예시: <프로젝트 진행 방식>\n내용1\n내용2\n<프로젝트의 현재 상황>\n내용1\n내용2\n<상세한 업무 내용>\n내용1\n내용2\n<참고자료 / 유의사항>\n내용1\n내용2
            * 제약 조건: 이 모든 데이터들은 json(Key-Value) 형식으로 전달해줘. Key는 proejctName, categoryId, categoryName, skillIdList, skillNameList, projectContent 로 해줘. 각각의 value 형식은 str, int, str, List[int], List[str], str 이야.
            """

            solar_payload = [
                {"role": "system", "content": chat_history[0]},
                {"role": "user", "content": "\n".join(chat_history[1:])},
                {"role": "user", "content": new_project_instruction + project_info}
            ]
            response = chat_with_solar(solar_payload)
            memory.chat_memory.add_message(HumanMessage(content="Solar 응답: " + json.dumps(response, ensure_ascii=False)))
            project_data = {**project_data.dict(), **response}
            memory.chat_memory.add_message(HumanMessage(content="새로운 프로젝트 정보: " + json.dumps(project_data, ensure_ascii=False)))

        except Exception as e:
            logging.error(f"Unexpected Error with Solar (Project Info Creation) | Error: {str(e)}")
            raise e

        # 4. 두번째 대화: 유사한 프로젝트 정보 생성
        try:
            project_list = ProjectService.get_project_similar(
                project_id=100000,
                category_id=project_data["categoryId"],
                budget=project_data["budget"],
                db=db,
                skill_list=project_data["skillIdList"]
            )
        except HTTPException as e:
            raise e

        try:
            sim_project_instruction = """
            등록하려는 프로젝트 정보와 유사한 프로젝트를 6개 찾아줘. 유사한 프로젝트의 기준은 projectContent가 유사하고 같은 스킬을 사용하는 게 우선이야.
            1) 유사한 프로젝트들의 duration, budget을 바탕으로 너가 예상하는 새로운 프로젝트의 duration별 expectedBudget 하나만 골라줘 (int)
            2) 유사한 프로젝트들의 minBudget (int)
            3) 유사한 프로젝트들의 maxBudget (int)
            4) 유사한 프로젝트들이 공통적으로 가지고 있는 skillName의 리스트인 simSkillNameList (최대 6개, List[str])
            5) 유사한 프로젝트들의 정보를 projectId, projectName, duration, budget, workType, contractType, status, registerDate, skillIdList, skillNameList, priority, locationName, categoryName를 Key로 하는 json(Key-Value) list 형태로 similar_projects라는 키의 value로 줘.
            * 제약 조건: 이 모든 데이터들은 json(Key-Value) 형식으로 전달해줘. Key는 similarProjects, expectedBudget, minBudget, maxBudget, simSkillNameList 로 해줘.
            """
            sim_project_data = json.dumps([project.__dict__ for project in project_list], ensure_ascii=False)
            memory.chat_memory.add_message(HumanMessage(content="유사한 프로젝트 조회 요청: " + sim_project_data))
            solar_payload = [
                {"role": "system", "content": chat_history[0]},  # 첫 번째 시스템 메시지
                {"role": "user", "content": "\n".join(chat_history[1:])},  # 이전 대화 내용 합치기
                {"role": "user", "content": sim_project_instruction + sim_project_data}
            ]
            response = chat_with_solar(solar_payload)
            memory.chat_memory.add_message(HumanMessage(content="Solar 응답(유사 프로젝트): " + json.dumps(response, ensure_ascii=False)))
        except Exception as e:
            logging.error(f"Unexpected Error with Solar (Similar Projects) | Error: {str(e)}")
            raise e

        return {**project_data, **response}

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
        project_data: ProjectRequest,
        user_id: int,
        db: Session
    ):
        """
        프로젝트 매칭정보 저장 및 WebSocket 알림 전송

        Args:
            project_data (ProjectRequest): 프로젝트 기간, 내용 등을 포함한 요청 데이터
            user_id (int): 기업 ID
            db (Session): SQLAlchemy 데이터베이스 세션
        """
        # X 만들기
        query = db.query(
            Freelancer.id.label("freelancerId"),
            Freelancer.work_exp.label("freelancerExperience"),
            Freelancer.price.label("freelancerPrice"),
            func.LISTAGG(FreelancerSkill.skill_id, ",").within_group(FreelancerSkill.skill_id).label("freelancerSkills")
            .join(FreelancerSkill, Freelancer.freelancer_id == FreelancerSkill.freelancer_id)
            .group_by(Freelancer.freelancer_id, Freelancer.work_exp, Freelancer.price)
        ).all()

        df = pd.DataFrame(query, columns=["freelancer_id",
                                          "freelancer_experience",
                                          "freelancer_price",
                                          "freelancer_skills"])

        project_skills = ",".join(map(str, project_data.skillList))
        df = df.assign(
            project_id=project_data.projectId,
            project_budget=project_data.budget,
            project_skills=project_skills,
            project_category=project_data.categoryId
        )
        numerical_features = ["project_budget", "freelancer_experience", "freelancer_price"]
        categorical_features = ["project_skills", "project_category", "freelancer_skills"]
        features = numerical_features + categorical_features
        X = df[features]

        # 모델 로드
        file_path = download_model_file(
            repo_name="TaroSin/HRmony",
            file_name="model.pkl"
        )

        with open(file_path, "rb") as f:
            model = pickle.load(f)

        # 모델 예측
        predictions = model.predict(X)
        result_df = df[["project_id", "freelancer_id"]].copy()
        result_df["matching_score"] = predictions

        # 결과 저장
        try:
            for _, row in result_df.iterrows():
                new_entry = ProjectRanking(
                    project_id=row["project_id"],
                    freelancer_id=row["freelancer_id"],
                    matching_score=row["matching_score"]
                )
                db.add(new_entry)

            db.commit()

        except IntegrityError as e:
            db.rollback()
            logging.error(f"IntegrityError while creating ProjectMatching for project_id={row['project_id']} | Error: {str(e)}")

        except Exception as e:
            db.rollback()
            logging.error(f"Unexpected Error while creating ProjectMatching for project_id={row['project_id']} | Error: {str(e)}")

        # WebSocket으로 알림 전송
        notify_client(user_id, f"✅ 프로젝트 {project_data.projectId} 매칭이 완료되었습니다!")

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
            .join(Category, Project.category_id == Category.id)
            .join(Company, Project.company_id == Company.id)
            .join(ProjectSkill, Project.id == ProjectSkill.project_id)
            .join(Skill, ProjectSkill.skill_id == Skill.id)
            .outerjoin(Feedback, Project.id == Feedback.project_id)
            .filter(Project.status == 2)
        )

        error_message = ""
        # 프리랜서
        if search_type == 0:
            query = query.filter(Project.freelancer_id == user_id)
            error_message = f"프리랜서({user_id})의 프로젝트 리스트"
        # 기업
        elif search_type == 1:
            query = query.filter(Project.company_id == user_id)
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
                Company.name
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

        project_ids = [project._mapping["projectId"] for project in projects]
        feedback_rows = (
            db.query(Feedback.project_id, Feedback.content)
            .filter(Feedback.project_id.in_(project_ids))
            .all()
        )
        feedback_dict = {row.project_id: row.content for row in feedback_rows}

        # CLOB -> str
        processed_projects = []
        for project in projects:
            project_dict = dict(project._mapping)
            fc = feedback_dict.get(project_dict["projectId"])
            if fc is not None and hasattr(fc, "read"):
                project_dict["feedbackContent"] = fc.read()
                project_dict["feedbackContent"] = project_dict["feedbackContent"].replace("\\n", "\n")
            else:
                project_dict["feedbackContent"] = fc
            processed_projects.append(ProjectFeedbackResponse(**project_dict))

        return processed_projects

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
            for skill_id in feedback_data.skillIdList:
                db.execute(
                    update(FreelancerSkill)
                    .where(
                        FreelancerSkill.freelancer_id == feedback_data.freelancerId,
                        FreelancerSkill.skill_id == skill_id
                    )
                    .values(skill_score=func.least(
                        func.greatest(FreelancerSkill.skill_score * 0.8 + feedback_data.expertise * 0.2, 0), 5)
                    )
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

        return CompanyResponse(**dict(company._mapping))

    def get_project_progress(
        freelancer_id: int,
        db: Session
    ) -> ProjectProgressResponse:
        """
        프리랜서 상세 조회(프로젝트 진행상황)

        Args:
            freelancer_id (int): 프리랜서 ID
            db (Session): SQLAlchemy 데이터베이스 세션

        Returns:
            ProjectProgressResponse: 조회된 프리랜서 진행상황 정보
        """
        progress = (
            db.query(
                func.count(Project.freelancer_id).label("projectCount"),
                func.coalesce(func.sum(
                    case(
                        (Project.status == 1, 1),
                        else_=0
                    )
                ), 0).label("ongoingCount"),
                func.coalesce(func.sum(
                    case(
                        (Project.status == 2, 1),
                        else_=0
                    )
                ), 0).label("completedCount")
            ).filter(Project.freelancer_id == freelancer_id)
            .first()
        )

        if not progress:
            raise HTTPException(
                status_code=ERROR_MESSAGES["NOT_FOUND"]["status"],
                detail=ERROR_MESSAGES["NOT_FOUND"]["message"].format(f"프리랜서({freelancer_id})의 프로젝트 진행상황")
            )

        return ProjectProgressResponse(**progress._mapping)
