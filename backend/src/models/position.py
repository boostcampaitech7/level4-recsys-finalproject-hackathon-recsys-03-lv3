from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.db import Base

class Position(Base):
    __tablename__ = "POSITION"

    id = Column("POSITION_ID", Integer, primary_key=True, index=True)
    name = Column("POSITION_NAME", String(50), nullable=False)

    # 관계 정의
    users = relationship("User", back_populates="position")