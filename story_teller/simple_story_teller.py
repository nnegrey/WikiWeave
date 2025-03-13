"""Extends the StoryStrategy to Generate the story"""

import os
import pprint
from dotenv import load_dotenv
from openai import OpenAI

from story_teller import story_strategy
from json_data import json_loader


class SimpleStoryTeller(story_strategy.StoryStrategy):
    """Porivdes a baseline story teller"""

    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.environ.get("OPEN_AI_TEST_API_KEY"))
        print("***** Simple Story Formatter *****")
        self.json_loader = json_loader.JsonLoader()

    def generate_story(self, evolutionary_links, call_openai=False):
        """Generates a story using the OpenAI API."""
        prompt_messages = self.__format_the_prompt(evolutionary_links)
        print("Simple Story Formatter Prompt Messages:")
        for i, m in enumerate(prompt_messages):
            print(f"\t{i}: {m['content']}")

        response = None
        if call_openai:
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                store=True,
                messages=prompt_messages,
            )
            print(completion.choices[0].message.content)
            response = {"content": completion.choices[0].message.content}
        else:
            response = self.__get_canned_response()
        pprint.pprint(response["content"])
        return response

    def __format_the_prompt(self, evolutionary_links):
        json_prompt_data = self.json_loader.get_json("json_data/prompts/prompt.json")
        messages = []
        # Set up the Developer Role
        messages.append(
            {
                "role": "developer",
                "content": json_prompt_data["developer_role_content"],
            }
        )
        # Set up the Task
        messages.append(
            {
                "role": "user",
                "content": json_prompt_data["task_content"],
            },
        )
        # Set up the Guidelines
        messages.append(
            {
                "role": "user",
                "content": json_prompt_data["guidelines_content"],
            },
        )
        # TODO(nnegrey) Provide an example
        # Provide the success criteria
        messages.append(
            {
                "role": "user",
                "content": json_prompt_data["success_content"],
            },
        )
        # Provide the user input list of items
        messages.extend(
            {"role": "user", "content": f"Item {i + 1}: {item}"}
            for i, item in enumerate(evolutionary_links)
        )
        return messages

    def __get_canned_response(self):
        """Skip calls to OpenAI for faster development."""
        return self.json_loader.get_json(
            "json_data/sample_output/open_ai_simple_story_response.json"
        )
