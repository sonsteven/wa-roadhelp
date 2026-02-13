from fastapi import APIRouter, Query, Depends
from sqlalchemy import func
from app.core.database import get_db
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Optional
from app.models.traffic_collisions import TrafficCollision
from app.viz_specs import build_collisions_by_severity_spec, build_horizontal_bar_graph_spec, build_line_chart_spec


router = APIRouter(
    prefix="/viz",
    tags=["Visualizations"]
    )


@router.get("/collisions-by-severity", response_model=None)
def collisions_by_severity(
    location: Optional[str] = Query(None, description="Filter by location"),
    start_date: Optional[datetime] = Query(None, description="Filter by results after start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by results before end date"),
    db: Session = Depends(get_db)
) -> dict:
    """
    Returns a Vega spec (JSON) with data embedded for collisions grouped by severity.
    """

    return build_collisions_by_severity_spec(
        db,
        location=location,
        start_date=start_date,
        end_date=end_date
    )


#/most-dangerous-addr @parameter -> addr_type intersection, block, mid
@router.get("/most-dangerous-intersections", response_model=None)
def most_dangerous_intersections(
    metric: str = Query("harm", pattern="^(harm|count)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> dict:
    """
    Returns a Vega spec (JSON) with data embedded for most dangerous intersections.
    """

    return build_horizontal_bar_graph_spec(
        db,
        address_type_name="Intersection",
        metric=metric,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/most-dangerous-blocks", response_model=None)
def most_dangerous_blocks(
    metric: str = Query("harm", pattern="^(harm|count)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> dict:
    """
    Returns a Vega spec (JSON) with data embedded for most dangerous blocks.
    """

    return build_horizontal_bar_graph_spec(
        db,
        address_type_name="Block",
        metric=metric,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )


# Need to address NULL locations to make this work
@router.get("/most-dangerous-alleys", response_model=None)
def most_dangerous_alleys(
    metric: str = Query("harm", pattern="^(harm|count)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> dict:
    """
    Returns a Vega spec (JSON) with data embedded for most dangerous alleys.
    """

    return build_horizontal_bar_graph_spec(
        db,
        address_type_name="Alley",
        metric=metric,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )

# Consolidate /most-dangerous-... into one endpoint, use parameter for determining ADDR_TYPE (INTERSECTION, ALLEY, BLOCK)

@router.get("/collision-metrics-over-time", response_model=None)
def collision_metrics_over_time(
    metric: str = Query("collisions", pattern="^(collisions|injuries|serious_injuries|fatalities|harm)$"),
    interval: str = Query("month", pattern="^(day|week|month)$"),
    series: str = Query("none", pattern="^(none|severity)$"),
    location: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
) -> dict:
    """
    Returns a Vega spec line chart with data embedded for metric over time intervals.
    """
    if start_date is None:
        max_dt = db.query(func.max(TrafficCollision.occurred_at)).scalar()
        if max_dt is not None:
            start_date = max_dt - timedelta(days=1825)
            if end_date is None:
                end_date = max_dt
    
    return build_line_chart_spec(
        db,
        metric=metric,
        interval=interval,
        series=series,
        location=location,
        start_date=start_date,
        end_date=end_date,
    )