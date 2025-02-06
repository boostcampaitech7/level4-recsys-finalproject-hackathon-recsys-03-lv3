from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base


class Project(Base):
    __tablename__ = "PROJECT"

    id = Column("PROJECT_ID", Integer, primary_key=True, index=True)
    name = Column("PROJECT_NAME", String(4000), nullable=False)
    duration = Column("DURATION", Integer, nullable=False)
    budget = Column("BUDGET", Integer, nullable=False)
    work_type = Column("WORK_TYPE", Integer, nullable=False)
    contract_type = Column("CONTRACT_TYPE", Integer, nullable=False)
    priority = Column("PRIORITY", Integer, nullable=False)
    content = Column("PROJECT_CONTENT", Text, nullable=False)
    status = Column("STATUS", Integer, nullable=False)
    register_date = Column("REGISTER_DATE", String(10), nullable=False)

    # 외래 키
    category_id = Column("CATEGORY_ID", Integer, ForeignKey("CATEGORY.CATEGORY_ID"), nullable=False)
    freelancer_id = Column("FREELANCER_ID", Integer, ForeignKey("FREELANCER.FREELANCER_ID"))
    company_id = Column("COMPANY_ID", Integer, ForeignKey("COMPANY.COMPANY_ID"), nullable=False)

    # 관계 정의
    company = relationship(
        "Company",
        back_populates="projects",
        foreign_keys=[company_id]
    )
    category = relationship(
        "Category",
        back_populates="projects",
        foreign_keys=[category_id]
    )
    freelancer = relationship(
        "Freelancer",
        back_populates="projects",
        foreign_keys=[freelancer_id]
    )
    skills = relationship(
        "ProjectSkill",
        back_populates="project",
        foreign_keys="ProjectSkill.project_id"
    )
    rankings = relationship(
        "ProjectRanking",
        back_populates="project",
        foreign_keys="ProjectRanking.project_id"
    )
    applicants = relationship(
        "ProjectApplicants",
        back_populates="project",
        foreign_keys="ProjectApplicants.project_id"
    )
    feedbacks = relationship(
        "Feedback",
        back_populates="project",
        foreign_keys="Feedback.project_id"
    )
