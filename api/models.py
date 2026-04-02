from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Article(BaseModel):
    id: str
    title: str
    summary: Optional[str]
    source_url: str
    source_name: str
    category: Optional[str]
    ministry: Optional[str]
    state: Optional[str]
    language: Optional[str]
    published_at: Optional[datetime]
    scraped_at: Optional[datetime]
    tags: Optional[List[str]]


class ArticleList(BaseModel):
    data: List[Article]
    count: int
    page: int
    per_page: int
