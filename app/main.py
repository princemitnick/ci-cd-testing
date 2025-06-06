from fastapi import FastAPI
from app.routers.tasks import router

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "OK"}

app.include_router(router, prefix="/tasks")