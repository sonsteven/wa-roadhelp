import requests
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.traffic_collisions import TrafficCollision
from app.models.severity import Severity
from app.models.collision_type import CollisionType
from app.models.sdot_collision_type import SDOTCollisionType
from app.models.junction_type import JunctionType
from app.models.light_condition import LightCondition
from app.models.weather_condition import WeatherCondition
from app.models.road_condition import RoadCondition
from app.models.address_type import AddressType

BASE_URL = "https://services.arcgis.com/ZOyb2t4B0UYuYNYH/ArcGIS/rest/services/SDOT_Collisions_All_Years/FeatureServer/0/query"
BATCH_SIZE = 1000

def fetch_collisions(offset: int = 0) -> dict:
    """
    Fetch a batch of collision records from Seattle ArcGIS API.
    """

    # Query parameters sent to ArcGIS REST API
    params = {
        "where": "1=1", # Return all records
        "outFields": "*",   # All available fields for each record
        "f": "json",    # Format in json
        "resultOffset" : offset,    # Pagination offset
        "resultRecordCount": BATCH_SIZE,    # Number records to return
        "orderByFields": "INCKEY"   # Order by INCKEY
    }

    # Send GET request with params and return response JSON
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def get_or_create_by_code_desc(db, model, code, desc):
    """
    Helper function to get or create lookup table.
    """
    if code is None:
        code_value = None
    else:
        code_value = str(code)
    
    if desc is None:
        desc_value = None
    else:
        desc_value = desc

    if code_value:
        row = db.query(model).filter_by(code=code_value).first()
    elif desc_value:
        row = db.query(model).filter_by(desc=desc_value).first()
    else:
        return None
    
    if row is None:
        row = model(code=code_value or "Unknown", desc=desc_value or "Unknown")
        db.add(row)
        db.flush()
    
    return row.id

def get_or_create_by_name(db, model, name):
    if not name:
        return None
    
    row = db.query(model).filter_by(name=name).first()
    
    if row is None:
        row = model(name=name)
        db.add(row)
        db.flush()
    
    return row.id
        

def import_collisions():
    """
    Main import function that fetches collision data in batches,
    converts API records into ORM objects for mapping,
    and inserts them into PostgreSQL.
    """
    offset = 0
    db: Session = SessionLocal()

    try:
        # Loop while API returns records
        while True:
            data = fetch_collisions(offset)

            # Extract features from response 
            features = data.get("features", [])

            if not features:
                break

            # Loop over each feature (collision record)
            for feature in features:
                # Get feature attributes
                attrs = feature["attributes"]

                # Convert epoch time to PST date time
                utc_time = datetime.fromtimestamp(attrs["INCDATE"]/1000, tz=timezone.utc)
                pst_time = utc_time.astimezone(ZoneInfo("America/Los_Angeles"))

                # Create or get lookup tables
                severity_id = get_or_create_by_code_desc(
                    db=db,
                    model=Severity,
                    code=attrs["SEVERITYCODE"],
                    desc=attrs["SEVERITYDESC"]
                )

                sdot_collision_type_id = get_or_create_by_code_desc(
                    db=db,
                    model=SDOTCollisionType,
                    code=attrs["SDOT_COLCODE"],
                    desc=attrs["SDOT_COLDESC"]
                )

                collision_type_id = get_or_create_by_name(
                    db=db,
                    model=CollisionType,
                    name=attrs["COLLISIONTYPE"]
                )

                junction_type_id = get_or_create_by_name(
                    db=db,
                    model=JunctionType,
                    name=attrs["JUNCTIONTYPE"]
                )

                light_condition_id = get_or_create_by_name(
                    db=db,
                    model=LightCondition,
                    name=attrs["LIGHTCOND"]
                )

                weather_condition_id = get_or_create_by_name(
                    db=db,
                    model=WeatherCondition,
                    name=attrs["WEATHER"]
                )

                road_condition_id = get_or_create_by_name(
                    db=db,
                    model=RoadCondition,
                    name=attrs["ROADCOND"]
                )

                address_type_id = get_or_create_by_name(
                    db=db,
                    model=AddressType,
                    name=attrs["ADDRTYPE"]
                )

                # Create new ORM object mapped to traffic_collisions table
                collision = TrafficCollision(
                    inc_key=attrs["INCKEY"],
                    location=attrs["LOCATION"],
                    occurred_at=pst_time,
                    severity_id=severity_id,
                    sdot_collision_type_id=sdot_collision_type_id, 
                    collision_type_id=collision_type_id,
                    junction_type_id=junction_type_id,
                    light_condition_id=light_condition_id,
                    weather_condition_id=weather_condition_id,
                    road_condition_id=road_condition_id,
                    address_type_id=address_type_id,
                    person_count=attrs["PERSONCOUNT"],
                    ped_count=attrs["PEDCOUNT"],
                    pedcyl_count=attrs["PEDCYLCOUNT"],
                    veh_count=attrs["VEHCOUNT"],
                    injuries=attrs["INJURIES"],
                    serious_injuries=attrs["SERIOUSINJURIES"],
                    fatalities=attrs["FATALITIES"]
                )

                # Add object to session for insertion
                db.add(collision)

            # Commit session transaction
            db.commit()
            offset += BATCH_SIZE

    finally:
        db.close()


if __name__ == "__main__":
    import_collisions()
    
