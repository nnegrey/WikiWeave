"""Main"""

import argparse

from story_teller import simple_story
from story_teller import simple_story_formatter
from graph_traversal import graph_traversal


class Main:

    def __print_configurations(self, args):
        print(f"Start Item: {args.start_item}")
        print(f"Start Description: {args.start_description}")
        print(f"End Item: {args.end_item}")
        print(f"End Description: {args.end_description}")
        print("WikiWeave Configuration:")
        print(f"\tGraph Traversal Strategry: {args.graph_traversal}")
        print(f"\tStory Teller Strategy: {args.story_teller}")
        print(f"\tCall OpenAI: {args.call_openai}")

    def run(self, args):
        self.__print_configurations(args)

        print("Finding the linked path between the two items...")
        gt = graph_traversal.GraphTraversal(args.graph_traversal)
        items = gt.find_linked_path(args.start_item, args.end_item, args.call_openai)
        print("Linked Items: ", items)
        print("Weaving the story...")
        prompt_formatter = None
        if args.story_teller == "simple_story":
            prompt_formatter = simple_story_formatter.SimpleStoryFormatter()

        prompt = prompt_formatter.format(items)

        print(prompt)

        if args.call_openai:
            storyTeller = simple_story.StoryTeller()
            storyTeller.generate_story(prompt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--start_item", help="The start point item to generate a story"
    )
    parser.add_argument(
        "-sd",
        "--start_description",
        help="Additional information about the start item",
        default=None,
    )
    parser.add_argument(
        "-e", "--end_item", help="The target end point item in the evolutionary story"
    )
    parser.add_argument(
        "-ed",
        "--end_description",
        help="Additional information about the end item",
        default=None,
    )
    # Behavioral Changes to the program.
    parser.add_argument(
        "-gt", "--graph-traversal", help="Graph Traversal", default="link_generator"
    )
    parser.add_argument(
        "-st", "--story-teller", help="Prompt Formatter", default="simple_story"
    )
    parser.add_argument("-c", "--call_openai", help="Call OpenAI", default=False)

    Main().run(parser.parse_args())
