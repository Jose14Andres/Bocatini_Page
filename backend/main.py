from fastapi import FastAPI

from database import Base, engine
import models  # noqa: F401: registra los modelos en los metadatos de Base.


app = FastAPI(title="Bocatini API")


@app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/api/status")
def database_status() -> dict[str, str]:
    return {"estado": "Base de datos conectada"}
