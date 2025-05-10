"""Move argument parsing logic into a seprate file.""" ""

import argparse


def parse_args():
    """Handles how WikiWeave behaves"""

    parser = argparse.ArgumentParser(
        prog="WikiWeave",
        description="WikiWeave uses pre-fetched Wikipedia Articles to weave together a "
        "evolutionary narrative that tells a story of how A led to B",
    )

    # System Behavioral Configurations
    parser.add_argument(
        "-c",
        "--call_openai",
        help="Call OpenAI, otherwise mocks the responses",
        default=False,
    )

    args = parser.parse_args()
    return args
