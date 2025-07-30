from datetime import datetime
from beanie import Document
from typing import List, Optional

class Article(Document):
    user_id: str
    language: str
    region: str
    headline: str
    subheadline: str
    deleted: bool
    byline: str
    published_on: Optional[datetime]
    updated_on: Optional[datetime]
    image_urls: Optional[List[str]]
    body: List[str]
    tags: List[str]
    source_urls: Optional[List[str]]

    class Settings:
        name = "articles"