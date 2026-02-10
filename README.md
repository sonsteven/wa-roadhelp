# sea-roadinfo
Backend service for ingesting and querying Seattle traffic collision data.

This project ingests Seattle’s public collision dataset into a normalized PostgreSQL schema (fact + lookup tables) and exposes filterable and aggregated FastAPI endpoints, plus Vega-ready visualization specs so the data can be explored programmatically and charted quickly.

## Features
- Ingests collision data from Seattle open data portal (ArcGIS REST).
- Stores data in PostgreSQL using SQLAlchemy ORM (fact table + lookup tables).
- Provides filterable `/collisions` API + `/lookups/*` reference endpoints.
- `/collisions/stats/*` aggregate endpoints.
- `/viz/*` endpoints return Vega specs with embedded data (copy/paste into Vega editor).

## Tech Stack
- Python 3.14.2
- FastAPI 
- SQLAlchemy 2.0.45
- PostgreSQL
- Uvicorn
- psycopg

## Local Development
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1 # or activate.bat if CMD prompt
pip install -r requirements.txt
```

## Configuration
Create `/.env` from `.env.example`
- Set `DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DBNAME`

## Data Note
- Data source: Seattle open data (ArcGIS REST).
- Importer uses `BATCH_SIZE` (default `1000`) and increments `offset += BATCH_SIZE` per page.
- Reduce `BATCH_SIZE` if you hit timeouts/rate limits.

## Data Import
1) Create tables
```bash
python -m app.create_tables
```
2) Import Seattle collision data
```bash
python -m app.data_import.seattle_collisions
```

## Run
```bash
python -m uvicorn app.main:app --reload
```

## Example Endpoints
- `GET /health`
- `GET /collisions?limit=50&offset=0`
- `GET /collisions/{id}`
- `GET /lookups/severities`
- `GET /lookups/collision-types`
- `GET /collisions/stats/`
- `GET /collisions/stats/by-severity`
- `GET /viz/collisions-by-severity`
- `GET /viz/most-dangerous-intersections?metric=harm`

## Vega 
1) Call a `/viz/...` endpoint.
2) Copy the returned JSON.
3) Paste into Vega Editor to render the chart.

## Bruno (API Testing)
This repo includes a Bruno collection for quick manual API testing.
- Collection: `app/bruno/SEA-RoadInfo API/`
- Environment: `local`
    - `baseURL` = `http://127.0.0.1:8000`



