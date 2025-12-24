from fastapi import APIRouter
from src.api.routes.query import query_full_book, query_selected_text
from src.api.routes.query import FullBookQuery, SelectedTextQuery

router = APIRouter()

@router.post("/public/query/full")
async def public_full_query(payload: FullBookQuery):
    # directly call your existing logic
    return await query_full_book(payload)

@router.post("/public/query/selected")
async def public_selected_query(payload: SelectedTextQuery):
    # directly call your existing logic
    return await query_selected_text(payload)
