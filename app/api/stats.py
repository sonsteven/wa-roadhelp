from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from app.schemas.collision_stats import CollisionStatsSummaryOut, CollisionsStatsBySeverityOut
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.models import TrafficCollision, Severity

router = APIRouter(
    prefix="/collisions/stats",
    tags=["Collisions Stats"]
)

@router.get("/", response_model=CollisionStatsSummaryOut, response_model_exclude_none=True)
def get_collision_stats(
    location : Optional[str] = Query(None, description="Filter by location text"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    start_date: Optional[datetime] = Query(None, description="Filter by results after start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by results before end date"),
    db: Session = Depends(get_db),
):
    """
    Get summary stats for all collisions, can be filtered based on location, severity, and start/end date.
    Returns an aggregated query that returns one row with all the stats.
    """
    query = db.query(TrafficCollision)

    if location:
        query = query.filter(TrafficCollision.location.ilike(f"%{location}%"))
    if severity:
        query = query.join(TrafficCollision.severity).filter(Severity.desc.ilike(f"%{severity}%"))
    if start_date:
        query = query.filter(TrafficCollision.occurred_at >= start_date)
    if end_date:
        query = query.filter(TrafficCollision.occurred_at <= end_date)

    row = query.with_entities(
        func.count(TrafficCollision.id).label("total_collisions"),
        func.coalesce(func.sum(TrafficCollision.injuries), 0).label("total_injuries"),
        func.coalesce(func.sum(TrafficCollision.serious_injuries), 0).label("total_serious_injuries"),
        func.coalesce(func.sum(TrafficCollision.fatalities), 0).label("total_fatalities"),
        func.min(TrafficCollision.occurred_at).label("occurred_at_min"),
        func.max(TrafficCollision.occurred_at).label("occurred_at_max")
    ).one()

    return dict(row._mapping)


@router.get("/by-severity", response_model=list[CollisionsStatsBySeverityOut], response_model_exclude_none=True)
def get_collisions_stats_by_severity(
    location : Optional[str] = Query(None, description="Filter by location text"),
    start_date: Optional[datetime] = Query(None, description="Filter by results after start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by results before end date"),
    db: Session = Depends(get_db),
):
    """
    Get summary stats for all collisions by severity, can be filtered based on location and start/end date.
    Returns an aggregated query that returns one row per severity.
    """
    query = db.query(TrafficCollision)

    if location:
        query = query.filter(TrafficCollision.location.ilike(f"%{location}%"))
    if start_date:
        query = query.filter(TrafficCollision.occurred_at >= start_date)
    if end_date:
        query = query.filter(TrafficCollision.occurred_at <= end_date)

    total_collisions = func.count(TrafficCollision.id).label("total_collisions")

    rows = (query.join(TrafficCollision.severity).with_entities(
        Severity.id.label("severity_id"),
        Severity.code.label("severity_code"),
        Severity.desc.label("severity_desc"),
        total_collisions
    )
    .group_by(Severity.id, Severity.code, Severity.desc)
    .order_by(total_collisions.desc())
    .all()
    )

    return [dict(r._mapping) for r in rows]