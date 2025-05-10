from fastapi import APIRouter, HTTPException
from typing import List
from ..models.wiki import PageNode, WikiPath
from traversal import Traversal

router = APIRouter()


@router.get("/random-path", response_model=WikiPath)
async def get_random_path():
    """Get a random path between two Wikipedia pages."""
    try:
        traversal = Traversal()
        path = traversal.traverse()

        if not path or len(path) < 2:
            raise HTTPException(status_code=404, detail="No path found")

        return WikiPath(start_page=path[0], end_page=path[-1], path=path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/page/{page_id}", response_model=PageNode)
async def get_page(page_id: int):
    """Get a specific page by ID."""
    try:
        traversal = Traversal()
        # You'll need to add a method to get a single page
        page = traversal.get_page_by_id(page_id)
        if not page:
            raise HTTPException(status_code=404, detail="Page not found")
        return page
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
