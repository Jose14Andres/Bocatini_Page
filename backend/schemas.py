"""Esquemas Pydantic (v2) para serializar el menú.

Se exponen solo los campos que el cliente necesita para renderizar el menú.
`is_available` NO se expone: el filtrado de disponibilidad ocurre a nivel de
consulta (ver `crud`/endpoint), por lo que el frontend nunca recibe agotados.
"""

from pydantic import BaseModel, ConfigDict


class ProductOut(BaseModel):
    id: int
    name: str
    # SQLAlchemy devuelve Decimal desde Numeric(10, 2); lo exponemos como float
    # para que el frontend pueda formatearlo con toFixed(2) sin ambigüedad.
    price: float
    # Sub-encabezado y nota opcionales; None cuando el producto no los tiene.
    group: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CategoryOut(BaseModel):
    id: int
    name: str
    products: list[ProductOut]

    model_config = ConfigDict(from_attributes=True)
