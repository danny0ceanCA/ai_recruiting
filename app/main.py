from fastapi import FastAPI

from app import database
from app.api import router as api_router

app = FastAPI(title="Student Profile SaaS")

@app.on_event("startup")
async def startup_event():
    database.init()

app.include_router(api_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
