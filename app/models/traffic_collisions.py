from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base

class TrafficCollision(Base):
    __tablename__ = "traffic_collisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inc_key: Mapped[int] = mapped_column(Integer, unique=True, index=True)

    location: Mapped[str] = mapped_column(String(255), nullable=True)

    occurred_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    severity_id: Mapped[int] = mapped_column(ForeignKey("severity.id"), nullable=False, index=True)
    collision_type_id: Mapped[int] = mapped_column(ForeignKey("collision_type.id"), nullable=False, index=True)

    severity = relationship("Severity", back_populates="collisions")
    collision_type = relationship("CollisionType", back_populates="collisions")
