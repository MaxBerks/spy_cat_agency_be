from fastapi import FastAPI
from app.db import init_db
from app.routers import cats, missions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Spy Cat Agency API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(cats.router)
app.include_router(missions.router)

@app.get("/")
def root():
    return {"message": "Spy Cat Agency API"}
