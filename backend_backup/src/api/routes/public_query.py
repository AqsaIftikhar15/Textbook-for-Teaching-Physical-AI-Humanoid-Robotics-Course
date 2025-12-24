from fastapi import APIRouter
from src.api.routes.query import query_full_book
from src.api.routes.query import FullBookQuery

router = APIRouter()

@router.post("/public/query/full")
async def public_full_query(payload: FullBookQuery):
    # directly call your existing logic
    return await query_full_book(payload)
