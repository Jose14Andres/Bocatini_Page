"""Script de sembrado (seeding) para el menú de Bocatini.

Crea las tablas en la base de datos (si no existen) y las puebla con el menú
real del restaurante. Es idempotente: limpia los datos existentes de productos
y categorías antes de insertar, de modo que puede ejecutarse varias veces sin
generar registros duplicados.

Uso (dentro del contenedor de Docker):
    docker compose exec backend python seed.py
"""

from decimal import Decimal

from database import Base, SessionLocal, engine
from models import Category, Product


# Estructura del menú: cada categoría con su lista de productos.
# Cada producto es (nombre, precio, is_available, group, description):
#   - group        -> sub-encabezado dentro de la categoría (None si no aplica).
#   - description  -> nota secundaria bajo el nombre (None si no aplica).
# El precio se declara como string y se convierte a Decimal para casar
# exactamente con la columna Numeric(10, 2) y evitar imprecisiones de flotante.
# El orden de inserción define el orden de visualización (se ordena por id).
MENU: dict[str, list[tuple[str, str, bool, str | None, str | None]]] = {
    "Bebidas calientes": [
        ("Morocho", "2.00", True, None, None),
        ("Chocolate", "2.00", True, None, None),
        ("Café en leche", "2.00", True, "Café", None),
        ("Café pintado", "1.50", True, "Café", None),
        ("Capuchino", "2.50", True, "Café", None),
    ],
    "Bebidas frías": [
        ("Jugo de naranja", "2.00", True, None, None),
        ("Naranjilla", "1.50", True, "Jugos varios", None),
        ("Mora", "1.50", True, "Jugos varios", None),
        ("Tomate de árbol", "1.50", True, "Jugos varios", None),
        ("Naranjilla", "2.00", True, "Batidos", None),
        ("Mora", "2.00", True, "Batidos", None),
        ("Tomate de árbol", "2.00", True, "Batidos", None),
    ],
    "Almuerzos": [
        (
            "Almuerzo del día",
            "3.25",
            True,
            None,
            "Sopa · Segundo · Jugo · disponible para llevar",
        ),
    ],
    "Lo Mejor de la casa": [
        ("Tortillas de maíz", "0.50", True, "Recomendado", None),
        ("Tortillas de trigo", "1.00", True, "Recomendado", None),
        ("Empanadas de viento", "0.25", True, "Recomendado", None),
        ("Tamal lojano", "1.50", True, "Envueltos tradicionales", "Pollo"),
        ("Humita", "1.00", True, "Envueltos tradicionales", "Dulce y salado"),
        ("Quimbolito", "1.00", True, "Envueltos tradicionales", None),
        (
            "Empanadas de pollo, carne o queso",
            "1.60",
            True,
            "Empanadas",
            None,
        ),
    ],
}


def seed() -> None:
    # 1. Recrea el esquema desde cero. Como el proyecto no usa migraciones
    #    (Alembic), un drop + create garantiza que las columnas nuevas del
    #    modelo (group, description) se apliquen aunque la tabla ya existiera.
    #    El seed ya era destructivo, así que esto no cambia su contrato.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        # 2. Inserta categorías y sus productos en orden de declaración.
        total_products = 0
        for category_name, products in MENU.items():
            category = Category(name=category_name)
            session.add(category)
            session.flush()  # Obtiene category.id antes del commit final.

            for name, price, is_available, group, description in products:
                session.add(
                    Product(
                        name=name,
                        price=Decimal(price),
                        is_available=is_available,
                        group=group,
                        description=description,
                        category_id=category.id,
                    )
                )
                total_products += 1

        session.commit()
        print(
            f"Sembrado completado: {len(MENU)} categorías "
            f"y {total_products} productos insertados."
        )
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()
