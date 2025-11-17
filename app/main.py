from contextlib import asynccontextmanager

from apscheduler import schedulers
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis import asyncio as redis

from app.router import router
from base import run_migrations


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()

    redis_conf = redis.from_url("redis://cache")
    FastAPICache.init(RedisBackend(redis_conf), prefix="fastapi-cache")

    scheduler.add_job(clear_usd_cache, "cron", hour=14, minute=11)
    scheduler.start()
    yield

    await redis_conf.close()
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


app.include_router(router)

scheduler = AsyncIOScheduler()


async def clear_usd_cache():
    await FastAPICache.clear(namespace="usd")
