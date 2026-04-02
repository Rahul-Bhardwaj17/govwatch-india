from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from db import get_client

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/")
async def list_articles(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    ministry: Optional[str] = None,
    state: Optional[str] = None,
    language: Optional[str] = None,
    source: Optional[str] = None,
):
    client = get_client()
    offset = (page - 1) * per_page

    query = client.table("articles").select("*", count="exact")

    if category:
        query = query.eq("category", category)
    if ministry:
        query = query.ilike("ministry", f"%{ministry}%")
    if state:
        query = query.eq("state", state)
    if language:
        query = query.eq("language", language)
    if source:
        query = query.eq("source_name", source)

    result = query.order("published_at", desc=True).range(offset, offset + per_page - 1).execute()

    return {
        "data": result.data,
        "count": result.count,
        "page": page,
        "per_page": per_page
    }


@router.get("/{article_id}")
async def get_article(article_id: str):
    client = get_client()
    result = client.table("articles").select("*").eq("id", article_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Article not found")
    return result.data
