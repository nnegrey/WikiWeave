"""Main"""

import os
from dotenv import load_dotenv
from openai import OpenAI

import arg_parser
from story_teller import story_teller
from graph_traversal import graph_traversal
from embeddings import wiki_fetch
from knowledge_base import storage_layer


class Main:

    def __init__(self, client):
        self.client = client
        self.storage_layer = storage_layer.StorageLayer()

    def __print_configurations(self, args):
        print("***** Input *****")
        print(f"Start Item: {args.start_item}")
        print(f"Start Description: {args.start_description}")
        print(f"End Item: {args.end_item}")
        print(f"End Description: {args.end_description}")
        print("***** WikiWeave Configuration *****")
        print(f"\tGraph Traversal Strategry: {args.graph_traversal}")
        print(f"\tStory Teller Strategy: {args.story_teller}")
        print(f"\tCall OpenAI: {args.call_openai}")
        print("**********")

    def run(self, args):
        self.__print_configurations(args)

        print(
            f"Finding the linked path between the two items: {args.start_item}, {args.end_item}"
        )
        gt = graph_traversal.GraphTraversal(
            args.graph_traversal,
            self.client,
            self.storage_layer,
        )
        items = gt.find_linked_path(args.start_item, args.end_item, args.call_openai)
        print("\nLinked Items: ", items)
        print("\nWeaving the story...")
        st = story_teller.StoryTeller(args.story_teller)

        st.generate_story(items)


if __name__ == "__main__":
    args = arg_parser.parse_args()
    load_dotenv()
    openai_client = OpenAI(api_key=os.environ.get("OPEN_AI_TEST_API_KEY"))
    if args.generate_test_dataset:
        wiki_fetch.WikiFetch(openai_client).create_test_dataset()
    else:
        Main(openai_client).run(args)
