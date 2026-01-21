from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, selectinload
from app.models.traffic_collisions import TrafficCollision
from app.models.severity import Severity
from app.core.database import get_db
from app.schemas.collisions import PaginatedCollisionsOut, TrafficCollisionOut

router = APIRouter(
    prefix="/collisions",
    tags=["Traffic Collisions"]
)

@router.get("/", response_model=PaginatedCollisionsOut, response_model_exclude_none=True)
def read_collisions(
    # Query parameters
    location: Optional[str] = Query(None, description="Filter by county name"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    start_date: Optional[datetime] = Query(None, description="Filter by results after start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by results before end date"),
    # Pagination
    limit: int = Query(100, ge=1, le=1000, description="Max number of results to return"),
    offset: int = Query(0, ge=0, description="Number of rows to skip"),
    # Database session
    db: Session = Depends(get_db)
):
    """
    Get LEAN list of traffic collisions, optionally filtered by location, severity, and date range.
    Only includes nested severity + collision_type fields, does not expand all other lookup tables.
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


    # Total count before pagination
    total = query.count()

    # Eager loading severity and collision_types, preventing (N+1) queries
    items = (
        query.options(
            selectinload(TrafficCollision.severity),
            selectinload(TrafficCollision.collision_type),
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    # Return wrapper dict for pagination
    return {"total": total, "limit": limit, "offset": offset, "items": items}

@router.get("/{collision_id}", response_model=TrafficCollisionOut, response_model_exclude_none=True)
def read_collision_expanded(collision_id: int, db: Session = Depends(get_db)):
    """
    Get full traffic collision record by ID, expanding all lookup relationships.
    """

    # Query one collision by primary key and eager-load all relationships needed
    collision = (
        db.query(TrafficCollision).options(
            selectinload(TrafficCollision.severity),
            selectinload(TrafficCollision.collision_type),
            selectinload(TrafficCollision.sdot_collision_type),
            selectinload(TrafficCollision.junction_type),
            selectinload(TrafficCollision.light_condition),
            selectinload(TrafficCollision.weather_condition),
            selectinload(TrafficCollision.road_condition),
            selectinload(TrafficCollision.address_type),
        )
        .filter(TrafficCollision.id == collision_id)
        .first()
    )

    # Raise error if no collision found with given ID
    if collision is None:
        raise HTTPException(status_code=404, detail="Collision not found")

    return collision