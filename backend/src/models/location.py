from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.db import Base


class Location(Base):
    __tablename__ = "LOCATION"

    id = Column("LOCATION_ID", Integer, primary_key=True, index=True)
    name = Column("LOCATION_NAME", String(100), nullable=False)

    # 관계 정의
    freelancers = relationship(
        "Freelancer",
        back_populates="location",
        foreign_keys="Freelancer.location_id"
    )
    companies = relationship(
        "Company",
        back_populates="location",
        foreign_keys="Company.location_id"
    )
