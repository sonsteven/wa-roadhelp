# wa-roadhelp
Backend service for ingesting and querying Washington State traffic collision data.

## Tech Stack
- Python
- FastAPI

## Local Development

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1 # or activate.bat if CMD prompt
pip install -r requirements.txt
uvicorn app.main:app --reload