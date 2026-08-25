from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool

from database import Base, engine
import models  # noqa: F401: registra los modelos en los metadatos de Base.


@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_in_threadpool(Base.metadata.create_all, bind=engine)
    yield


app = FastAPI(title="Bocatini API", lifespan=lifespan)


@app.get("/api/status")
def database_status() -> dict[str, str]:
    return {"estado": "Base de datos conectada"}
