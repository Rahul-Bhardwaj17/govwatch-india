from fastapi import APIRouter, Query, HTTPException
from db import get_client

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/")
async def search_articles(
    q: str = Query(..., min_length=2),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    client = get_client()
    offset = (page - 1) * per_page

    result = client.table("articles").select("*", count="exact").text_search(
        "title,summary", q, config="english"
    ).order("published_at", desc=True).range(offset, offset + per_page - 1).execute()

    return {
        "data": result.data,
        "count": result.count,
        "query": q,
        "page": page,
        "per_page": per_page
    }
