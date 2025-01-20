from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base

class ProjectApplicants(Base):
    __tablename__ = "PROJECT_APPLICANTS"

    project_id = Column("PROJECT_ID", Integer, ForeignKey("PROJECT.PROJECT_ID"), primary_key=True)
    user_id = Column("USER_ID", Integer, ForeignKey("USER.USER_ID"), primary_key=True)

    # 관계 정의
    project = relationship("Project", back_populates="project_applicants")
    user = relationship("User", back_populates="project_applicants")