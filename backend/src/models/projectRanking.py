from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base


class ProjectRanking(Base):
    __tablename__ = "PROJECT_RANKING"

    project_id = Column("PROJECT_ID", Integer, ForeignKey("PROJECT.PROJECT_ID"), primary_key=True)
    freelancer_id = Column("FREELANCER_ID", Integer, ForeignKey("FREELANCER.FREELANCER_ID"), primary_key=True)
    matching_score = Column("MATCHING_SCORE", Float, nullable=False)

    # 관계 정의
    project = relationship(
        "Project",
        back_populates="rankings",
        foreign_keys=[project_id]
    )
    freelancer = relationship(
        "Freelancer",
        back_populates="rankings",
        foreign_keys=[freelancer_id]
    )
