from fastapi import FastAPI
from app.db import init_db

app = FastAPI(title="Spy Cat Agency API")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Spy Cat Agency API"}
