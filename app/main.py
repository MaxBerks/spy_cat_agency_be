from fastapi import FastAPI

app = FastAPI(title="Spy Cat Agency API")

@app.get("/")
def root():
    return {"message": "Spy Cat Agency API"}
