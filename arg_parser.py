"""Move argument parsing logic into a seprate file.""" ""

import argparse


def parse_args():
    """Handles how WikiWeave behaves"""

    parser = argparse.ArgumentParser(
        prog="WikiWeave",
        description="WikiWeave uses pre-fetched Wikipedia Articles to weave together a "
        "evolutionary narrative that tells a story of how A led to B",
    )

    # Graph Traversal / Story Teller Component Selection
    parser.add_argument(
        "-gt",
        "--graph-traversal",
        help="Graph Traversal Stratigies: [link_generator, embedding_traversal, random_traversal]",
        default="link_generator",
    )
    parser.add_argument(
        "-st",
        "--story-teller",
        help="Story Teller Stratigies: [simple_story]",
        default="simple_story",
    )

    # Story Inputs
    parser.add_argument(
        "-s", "--start_item", help="The start point item to generate a story"
    )
    parser.add_argument(
        "-sd",
        "--start_description",
        help="[Optional] Additional information about the start item",
        default=None,
    )
    parser.add_argument(
        "-e", "--end_item", help="The target end point item in the evolutionary story"
    )
    parser.add_argument(
        "-ed",
        "--end_description",
        help="[Optional] Additional information about the end item",
        default=None,
    )

    # System Behavioral Configurations
    parser.add_argument(
        "-c",
        "--call_openai",
        help="Call OpenAI, otherwise mocks the responses",
        default=False,
    )
    parser.add_argument(
        "-gtd",
        "--generate_test_dataset",
        help="Generates a test dataset",
        default=False,
    )

    args = parser.parse_args()
    __print_configurations(args)
    return args


def __print_configurations(args):
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
