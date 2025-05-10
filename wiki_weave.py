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

    def weave(self, args):
        """Weaves an evolutionary tale given the input and selected configuration"""
        items = traversal.Traversal().traverse()

        print(f"\nFound {len(items)} items in the path.")

        if args.call_openai:
            print("\nWeaving the story...")
            story_teller.StoryTeller().weave_story(items)
        else:
            print("\nSkipping call to OpenAI. No story generated.")


if __name__ == "__main__":
    args = arg_parser.parse_args()
    load_dotenv()
    openai_client = OpenAI(api_key=os.environ.get("OPEN_AI_TEST_API_KEY"))
    WikiWeave(openai_client).weave(args)
