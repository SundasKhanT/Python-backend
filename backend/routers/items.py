from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, field_validator
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from backend.db.database import SessionLocal
from backend.models.items import Item
from backend.config import ITEMS_PREFIX, ITEMS_INGEST

router = APIRouter(prefix=ITEMS_PREFIX, tags=["Items"])


async def get_db():
    async with SessionLocal() as session:
        yield session


class ItemIn(BaseModel):
    name: str
    category: str
    value: float

    @field_validator("name", "category")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("must not be empty")
        return v.strip()

    @field_validator("value")
    def positive_value(cls, v):
        if v <= 0:
            raise ValueError("must be positive")
        return v


@router.post(ITEMS_INGEST.replace(ITEMS_PREFIX, ""))
async def ingest_items(items: List[ItemIn], db: AsyncSession = Depends(get_db)):
    results = {"success": [], "errors": []}
    db_items = []

    for item in items:
        if not item.name.strip() or not item.category.strip() or item.value <= 0:
            results["errors"].append(
                {"name": item.name, "category": item.category, "error": "Invalid input"}
            )
            continue

        if item.category.lower() == "premium" and item.value < 100:
            results["errors"].append(
                {
                    "name": item.name,
                    "category": item.category,
                    "error": "Premium items must have value >= 100",
                }
            )
            continue

        db_item = Item(name=item.name, category=item.category, value=item.value)
        db.add(db_item)
        db_items.append(db_item)

    try:
        if db_items:
            await db.flush()
            await db.commit()

            for db_item in db_items:
                results["success"].append(
                    {
                        "id": db_item.item_id,
                        "name": db_item.name,
                        "category": db_item.category,
                        "value": db_item.value,
                    }
                )
    except SQLAlchemyError as e:
        await db.rollback()
        results["errors"].append({"error": str(e)})

    return results
