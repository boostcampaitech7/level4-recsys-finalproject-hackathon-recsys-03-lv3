from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base

class User(Base):
    __tablename__ = "USER"

    id = Column("USER_ID", Integer, primary_key=True, index=True)
    email = Column("EMAIL", String(100), unique=True, nullable=False)
    password = Column("PASSWORD", String(100), nullable=False)
    name = Column("USER_NAME", String(100), nullable=False)
    work_exp = Column("WORK_EXP", Integer, nullable=False)
    contact = Column("CONTACT", String(20), nullable=True)

    # 외래 키
    team_id = Column("TEAM_ID", Integer, ForeignKey("TEAM.TEAM_ID"), nullable=False)
    rank_id = Column("RANK_ID", Integer, ForeignKey("RANK.RANK_ID"), nullable=False)
    role_id = Column("ROLE_ID", Integer, ForeignKey("ROLE.ROLE_ID"), nullable=False)
    position_id = Column("POSITION_ID", Integer, ForeignKey("POSITION.POSITION_ID"), nullable=False)

    # 관계 정의
    team = relationship("Team", back_populates="users")
    rank = relationship("Rank", back_populates="users")
    role = relationship("Role", back_populates="users")
    position = relationship("Position", back_populates="users")
    projects = relationship("Project", back_populates="user")
    project_applicants = relationship("ProjectApplicants", back_populates="user")
    task_rankings = relationship("TaskRanking", back_populates="user")
    task_participants = relationship("TaskParticipants", back_populates="user")
    user_skills = relationship("UserSkill", back_populates="user")
    