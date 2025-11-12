from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.router import router
from base import run_migrations


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(router)
