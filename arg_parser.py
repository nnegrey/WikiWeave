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
        help="Graph Traversal Stratigies: [link_generator, embedding_traversal]",
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

    return parser.parse_args()
