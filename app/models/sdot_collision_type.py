from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base

class SDOTCollisionType(Base):
    __tablename__ = "sdot_collision_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    desc: Mapped[str] = mapped_column(String(255), nullable=True) 

    collisions = relationship("TrafficCollision", back_populates="sdot_collision_type")

