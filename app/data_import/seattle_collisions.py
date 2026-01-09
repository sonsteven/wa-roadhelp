import requests
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.traffic_collisions import TrafficCollision

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

                # Create new ORM object mapped to traffic_collisions table
                collision = TrafficCollision(
                    inc_key=attrs["INCKEY"],
                    severity=attrs["SEVERITYDESC"],
                    location=attrs["LOCATION"],
                    occurred_at=datetime.utcnow()   # Temporary, need to parse collision timestamp
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
    

