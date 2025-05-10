from pydantic import BaseModel
from typing import List, Optional


class PageNode(BaseModel):
    id: int
    title: str
    summary: str
    embedding: List[float]


class WikiPath(BaseModel):
    start_page: PageNode
    end_page: PageNode
    path: List[PageNode]
