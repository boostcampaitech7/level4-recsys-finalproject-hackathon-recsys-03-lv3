from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base


class ProjectApplicants(Base):
    __tablename__ = "PROJECT_APPLICANTS"

    project_id = Column("PROJECT_ID", Integer, ForeignKey("PROJECT.PROJECT_ID"), primary_key=True)
    freelancer_id = Column("FREELANCER_ID", Integer, ForeignKey("FREELANCER.FREELANCER_ID"), primary_key=True)

    # 관계 정의
    project = relationship(
        "Project",
        back_populates="applicants",
        foreign_keys=[project_id]
    )
    freelancer = relationship(
        "Freelancer",
        back_populates="applicants",
        foreign_keys=[freelancer_id]
    )
