from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.db import Base


class Rank(Base):
    __tablename__ = "RANK"

    id = Column("RANK_ID", Integer, primary_key=True, index=True)
    name = Column("RANK_NAME", String(50), nullable=False)

    # 관계 정의
    users = relationship(
        "User",
        back_populates="rank",
        foreign_keys="User.rank_id"
    )
