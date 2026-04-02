from fastapi import APIRouter
from db import get_client

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("/")
async def list_sources():
    client = get_client()
    result = client.table("sources").select("*").eq("is_active", True).execute()
    return result.data
