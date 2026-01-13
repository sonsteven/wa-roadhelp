from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.models.traffic_collisions import TrafficCollision
from app.models.severity import Severity
from app.core.database import get_db

router = APIRouter(
    prefix="/collisions",
    tags=["Traffic Collisions"]
)

@router.get("/")
def read_collisions(
    location: Optional[str] = Query(None, description="Filter by county name"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    start_date: Optional[datetime] = Query(None, description="Filter by results after start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by results before end date"),
    limit: int = Query(100, ge=1, le=1000, description="Max number of results to return"),
    offset: int = Query(0, ge=0, description="Number of rows to skip"),
    db: Session = Depends(get_db)
):
    """
    Get traffic collisions, optionally filtered by county, severity, and date range.
    """

    query = db.query(TrafficCollision)

    # Apply filters
    if location:
        query = query.filter(TrafficCollision.location.ilike(f"%{location}%"))
    if severity:
        query = query.join(TrafficCollision.severity).filter(Severity.desc.ilike(f"%{severity}%"))
    if start_date:
        query = query.filter(TrafficCollision.occurred_at >= start_date)
    if end_date:
        query = query.filter(TrafficCollision.occurred_at <= end_date)

    # Apply pagination
    query = query.offset(offset).limit(limit)

    return query.all()


