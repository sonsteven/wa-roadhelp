from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.traffic_collision import TrafficCollision
from app.core.database import get_db

router = APIRouter(
    prefix="/collisions",
    tags=["Traffic Collisions"]
)

@router.get("/")
def read_collisions(db: Session = Depends(get_db)):
    """
    Get all traffic collisions.    
    """
    collisions = db.query(TrafficCollision).all()
    return collisions