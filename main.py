"""Main"""

import argparse

from story_teller import simple_story
from prompts import simple_story_formatter


class Main:

    def run(self, formatter, call_openai, gitems):
        print("formatter:", formatter)
        print("call_openai:", call_openai)
        print("items:", items)
        prompt_formatter = None
        if formatter == "simple_story":
            prompt_formatter = simple_story_formatter.SimpleStoryFormatter()

        prompt = prompt_formatter.format(items)

        print(prompt)

        if call_openai:
            storyTeller = simple_story.StoryTeller()
            storyTeller.generate_story(prompt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--formatter", help="Prompt Formatter", default="simple_story"
    )
    parser.add_argument("-c", "--call", help="Call OpenAI", default=False)
    parser.add_argument(
        "-i", "--items", nargs="+", help="List of items to generate a story"
    )
    args = parser.parse_args()
    Main().run(args.formatter, args.call, args.items)
