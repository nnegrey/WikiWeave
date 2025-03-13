"""Simple Main to either weave the story or interact with the database"""

import os
from dotenv import load_dotenv
from openai import OpenAI

import arg_parser
import wiki_weave
from embeddings import wiki_fetch


if __name__ == "__main__":
    args = arg_parser.parse_args()
    load_dotenv()
    openai_client = OpenAI(api_key=os.environ.get("OPEN_AI_TEST_API_KEY"))
    if args.generate_test_dataset:
        wiki_fetch.WikiFetch(openai_client).create_test_dataset()
    else:
        wiki_weave.WikiWeave(openai_client).weave(args)
