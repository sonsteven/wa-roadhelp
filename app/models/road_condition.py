from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base

class RoadCondition(Base):
    __tablename__ = "road_condition"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(300), nullable=False, unique=True)

    collisions = relationship("TrafficCollision", back_populates="road_condition") 