from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from backend.schemas.items import ItemCreate
from backend.models.items import Item as ItemModel


router = APIRouter()


@router.post("/api/v1/items/ingest")
async def ingest_items(items: List[ItemCreate], db: AsyncSession = Depends(get_db)):
    errors = []
    valid_items = []

    for i, item in enumerate(items):
        if item.category == "Premium" and item.value < 100:
            errors.append(
                {
                    "index": i,
                    "item_id": item.item_id,
                    "error": "Premium items must have value >= $100",
                }
            )
            continue

        db_item = ItemModel(
            item_id=item.item_id,
            name=item.name,
            category=item.category,
            value=item.value,
        )
        valid_items.append(db_item)

    if errors:
        raise HTTPException(status_code=422, detail=errors)

    db.add_all(valid_items)
    await db.commit()

    return {"ingested": len(valid_items), "errors": errors}
