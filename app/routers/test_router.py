from fastapi import APIRouter

import asyncio

router = APIRouter()

@router.get("/test/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    await asyncio.sleep(5)
    return {"item_id": item_id, "q": q}