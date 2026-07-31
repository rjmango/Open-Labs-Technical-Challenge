from fastapi import FastAPI
import models
from database import engine
from routers import notes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(notes.router)

@app.get("/health")
def get_status():
    return {"status": "ok"}