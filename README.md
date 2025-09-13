# Spy Cat Agency — Backend

REST API for managing spy cats, their missions, and targets.

## Stack
- FastAPI, Uvicorn
- SQLAlchemy (SQLite)
- Pydantic v2
- httpx (breed validation via TheCatAPI)
- CORS (for frontend at http://localhost:3000)

## Quick Start
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Docs (Swagger): http://127.0.0.1:8000/docs

Postman collection: [link](https://www.postman.com/sca999-8039/spy-cats-agency/collection/r6uv6ty/spy-cat-agency?action=share&creator=41330662)