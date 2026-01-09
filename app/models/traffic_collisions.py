from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base

class TrafficCollision(Base):
    __tablename__ = "traffic_collisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inc_key: Mapped[int] = mapped_column(Integer, unique=True, index=True)

    location: Mapped[str] = mapped_column(String(100), nullable=True)
    severity: Mapped[str] = mapped_column(String(100), nullable=False)

    occurred_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)


