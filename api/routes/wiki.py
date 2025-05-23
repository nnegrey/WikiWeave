from fastapi import APIRouter, HTTPException
from traversal import Traversal
from wiki_weave import WikiWeave
from ..models.wiki import WikiPath, WovenStory
from openai import OpenAI
import os

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


@router.get("/woven-story", response_model=WovenStory)
async def get_woven_story():
    """Get a woven story."""
    try:
        client = OpenAI(api_key=os.environ.get("OPEN_AI_TEST_API_KEY"))
        woven_story = WikiWeave(client).weave(call_openai=True)
        return WovenStory(**woven_story)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
