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
import asyncio
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
from database import Base, engine


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
