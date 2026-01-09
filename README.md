# sea-roadinfo
Backend service for ingesting and querying Seattle traffic collision data.
- Ingests real collision data from Seattle City open data portal.
- Stores in PostgreSQL via SQLAlchemy ORM.
- Provides filterable APIs for querying by location, date, severity, etc.

## Tech Stack
- Python 3.14.2
- FastAPI 
- SQLAlchemy 2.0.45
- PostgreSQL 
- Uvicorn

## Local Development

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1 # or activate.bat if CMD prompt
pip install -r requirements.txt
uvicorn app.main:app --reload