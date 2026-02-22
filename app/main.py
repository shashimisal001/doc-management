from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.api import api_router

@asynccontextmanager
async def lifespan(current_app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def home():
    return {"message": "Document manager apis - v1"}

app.include_router(api_router, prefix="/api/v1")