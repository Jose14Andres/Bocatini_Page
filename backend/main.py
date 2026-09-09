import os

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, contains_eager

from database import Base, engine, get_db
import models
import schemas


app = FastAPI(title="Bocatini API")

# --- CORS -------------------------------------------------------------------
# Necesario SOLO cuando el navegador del cliente llama al backend directamente
# (fetch desde el componente cliente hacia http://localhost:8000).
# Si el fetch se hace server-side (Server Component -> http://backend:8000),
# es tráfico contenedor-a-contenedor y CORS ni siquiera interviene.
# Los orígenes se leen de una variable de entorno separada por comas.
_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/api/status")
def database_status() -> dict[str, str]:
    return {"estado": "Base de datos conectada"}


@app.get("/api/menu", response_model=list[schemas.CategoryOut])
def get_menu(db: Session = Depends(get_db)) -> list[models.Category]:
    """Devuelve todas las categorías con sus productos DISPONIBLES anidados.

    Regla de negocio: solo se devuelven productos con is_available == True.
    El filtro se aplica a NIVEL DE CONSULTA usando el ON de un OUTER JOIN
    (Category.products.and_(...)) + contains_eager, de modo que:
      - los agotados nunca salen de la base de datos, y
      - las categorías sin productos disponibles siguen apareciendo (vacías).
    """
    categories = (
        db.query(models.Category)
        .outerjoin(
            models.Category.products.and_(models.Product.is_available.is_(True))
        )
        .options(contains_eager(models.Category.products))
        .order_by(models.Category.id, models.Product.id)
        .all()
    )
    return categories
