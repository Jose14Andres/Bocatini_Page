import time
from decimal import Decimal
from database import Base, SessionLocal, engine
from models import Category, Product

# Make a very large menu
MENU = {
    f"Category_{i}": [
        (f"Product_{i}_{j}", "1.00", True) for j in range(1000)
    ] for i in range(10)
}

def seed_original():
    # 1. Asegura que las tablas existan.
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        session.query(Product).delete()
        session.query(Category).delete()
        session.commit()

        start = time.time()
        total_products = 0
        for category_name, products in MENU.items():
            category = Category(name=category_name)
            session.add(category)
            session.flush()

            for name, price, is_available in products:
                session.add(
                    Product(
                        name=name,
                        price=Decimal(price),
                        is_available=is_available,
                        category_id=category.id,
                    )
                )
                total_products += 1

        session.commit()
        end = time.time()
        return end - start
    finally:
        session.close()

def seed_optimized():
    # 1. Asegura que las tablas existan.
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        session.query(Product).delete()
        session.query(Category).delete()
        session.commit()

        start = time.time()
        total_products = 0
        all_products = []
        for category_name, products in MENU.items():
            category = Category(name=category_name)
            session.add(category)
            session.flush()

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
        end = time.time()
        return end - start
    finally:
        session.close()

if __name__ == "__main__":
    t_orig = seed_original()
    print(f"Original: {t_orig:.4f}s")
    t_opt = seed_optimized()
    print(f"Optimized: {t_opt:.4f}s")
