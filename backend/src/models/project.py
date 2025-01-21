from sqlalchemy import Column, Integer, String, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from api.db import Base


class Project(Base):
    __tablename__ = "PROJECT"

    id = Column("PROJECT_ID", Integer, primary_key=True, index=True)
    name = Column("PROJECT_NAME", String(100), nullable=False)
    content = Column("PROJECT_CONTENT", String(4000), nullable=False)
    start_date = Column("START_DATE", String(8), nullable=True)
    end_date = Column("END_DATE", String(8), nullable=True)
    progress_status = Column("PROGRESS_STAUS", CHAR(1), nullable=False)

    # 외래 키
    team_id = Column("TEAM_ID", Integer, ForeignKey("TEAM.TEAM_ID"), nullable=False)
    user_id = Column("USER_ID", Integer, ForeignKey("USER.USER_ID"), nullable=False)

    # 관계 정의
    feedbacks = relationship(
        "Feedback",
        back_populates="project",
        foreign_keys="Feedback.project_id"
    )
    project_applicants = relationship(
        "ProjectApplicants",
        back_populates="project",
        foreign_keys="ProjectApplicants.project_id"
    )
    tasks = relationship(
        "Task",
        back_populates="project",
        foreign_keys="Task.project_id"
    )
    team = relationship(
        "Team",
        back_populates="projects",
        foreign_keys=[team_id]
    )
    user = relationship(
        "User",
        back_populates="projects",
        foreign_keys=[user_id]
    )
