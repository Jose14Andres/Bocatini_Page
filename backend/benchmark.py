import asyncio
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
from database import Base, engine
import models


@asynccontextmanager
async def lifespan_sync(app: FastAPI):
    # simulate some heavy work
    time.sleep(2)
    Base.metadata.create_all(bind=engine)
    yield

from starlette.concurrency import run_in_threadpool
@asynccontextmanager
async def lifespan_async(app: FastAPI):
    # simulate some heavy work
    await run_in_threadpool(time.sleep, 2)
    await run_in_threadpool(Base.metadata.create_all, bind=engine)
    yield

async def background_task():
    start = time.time()
    await asyncio.sleep(0.01) # a very small sleep to yield control
    end = time.time()
    return end - start

async def run_benchmark(lifespan_func):
    app = FastAPI(lifespan=lifespan_func)

    # We want to see if the lifespan function blocks the event loop
    # We will measure the delay of a simple async task running concurrently
    task = asyncio.create_task(background_task())

    # Give the task a tiny bit of time to start running and hit the sleep
    await asyncio.sleep(0.001)

    async with lifespan_func(app):
        pass

    delay = await task
    return delay

async def main():
    print("Running with sync lifespan...")
    delay_sync = await run_benchmark(lifespan_sync)
    print(f"Delay in background task (sync): {delay_sync:.3f}s")

    print("Running with async lifespan...")
    delay_async = await run_benchmark(lifespan_async)
    print(f"Delay in background task (async): {delay_async:.3f}s")

if __name__ == "__main__":
    asyncio.run(main())
