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
# Cada producto es (nombre, precio, is_available). El precio se declara como
# string y se convierte a Decimal para casar exactamente con la columna
# Numeric(10, 2) y evitar imprecisiones de coma flotante.
MENU: dict[str, list[tuple[str, str, bool]]] = {
    "Bebidas": [
        ("Morocho", "2.00", True),
        ("Chocolate", "2.00", True),
        ("Café", "1.25", True),
        ("Jugo de naranja", "2.00", True),
        ("Jugos varios", "1.50", True),
        ("Batidos", "2.00", True),
        ("Capuchino", "2.50", False),  # No disponible temporalmente.
    ],
    "Amasijos y Comida": [
        ("Tortillas de maiz", "0.50", True),
        ("Sanduche de Pernil Cuencano", "2.50", True),
        ("Tortillas de trigo", "1.00", True),
        ("Quimbolito", "1.00", True),
        ("Empanadas de viento", "0.25", True),
        ("Humitas", "1.00", True),
        ("Empanadas de Pollo, carne o queso", "1.60", True),
        ("Tamales", "1.50", True),
    ],
    "Almuerzos": [
        ("Almuerzos", "3.25", True),
    ],
}


def seed() -> None:
    # 1. Asegura que las tablas existan.
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        # 2. Limpia datos previos para que el script sea re-ejecutable.
        #    Se borran primero los productos por la restricción de clave foránea.
        session.query(Product).delete()
        session.query(Category).delete()
        session.commit()

        # 3. Inserta categorías y sus productos.
        total_products = 0
        for category_name, products in MENU.items():
            category = Category(name=category_name)
            session.add(category)
            session.flush()  # Obtiene category.id antes del commit final.

            category_products = [
                Product(
                    name=name,
                    price=Decimal(price),
                    is_available=is_available,
                    category_id=category.id,
                )
                for name, price, is_available in products
            ]
            session.add_all(category_products)
            total_products += len(category_products)

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
