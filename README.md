# Spy Cat API

FastAPI application to manage spy cats and their missions.

## Tech

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- httpx (for TheCatAPI)

## Setup

1. Clone the repo:

```bash
git clone https://github.com/tiron-vadym/SpyCat
cd SpyCatAgency
```
2. Create and activate a virtual environment:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Create .env with DATABASE_URL


5. Start server
```bash
uvicorn main:app --reload
```

[Spy Cat API Postman Collection](https://www.postman.com/payload-meteorologist-66152839/workspace/spycat/collection/32920802-2710911d-a1e5-45f8-9b75-a05878cb96c3?action=share&source=copy-link&creator=32920802)



