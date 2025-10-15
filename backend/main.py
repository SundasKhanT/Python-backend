from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.db.database import engine, Base
from backend.routers import items


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Python-backend API", lifespan=lifespan)
app.include_router(items.router)
