from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.db import Base

class Team(Base):
    __tablename__ = "TEAM"

    id = Column("TEAM_ID", Integer, primary_key=True, index=True)
    name = Column("TEAM_NAME", String(50), nullable=False)

    # 관계 정의
    users = relationship("User", back_populates="team")
    projects = relationship("Project", back_populates="team")
