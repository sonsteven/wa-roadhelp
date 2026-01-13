from app.core.database import engine
from app.core.base import Base

import app.models.traffic_collisions
import app.models.collision_type
import app.models.severity

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()