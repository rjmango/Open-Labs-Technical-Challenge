from fastapi import FastAPI
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
def get_status():
    return {"status": "ok"}