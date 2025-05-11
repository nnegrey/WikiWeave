"""WikiWeave Main"""

import os
from dotenv import load_dotenv
from openai import OpenAI

import arg_parser
import story_teller
import traversal


class WikiWeave:
    """Entry point to running WikiWeave"""

    def __init__(self, client):
        self.client = client

    def weave(self, call_openai=False):
        """Weaves an evolutionary tale given the input and selected configuration"""
        items = traversal.Traversal().traverse()
        story = None

        if call_openai:
            story = story_teller.StoryTeller().weave_story(items)

        return {"path": items, "story": story}


if __name__ == "__main__":
    args = arg_parser.parse_args()
    load_dotenv()
    openai_client = OpenAI(api_key=os.environ.get("OPEN_AI_TEST_API_KEY"))
    result = WikiWeave(openai_client).weave(args.call_openai)

    print(f"\nFound {len(result['path'])} items in the path.")
    if result["story"]:
        print("\nThe woven wiki:")
        print(result["story"]["content"])
