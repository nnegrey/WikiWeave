from pydantic import BaseModel
from typing import List, Optional


class PageNode(BaseModel):
    id: int
    title: str
    summary: str


class WikiPath(BaseModel):
    start_page: PageNode
    end_page: PageNode
    path: List[PageNode]


class WikiNode(BaseModel):
    id: int
    title: str
    summary: str


class WovenStory(BaseModel):
    nodes: List[WikiNode]
    story: Optional[dict] = None
