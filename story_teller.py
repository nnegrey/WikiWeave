"""Extends the StoryStrategy to Generate the story"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import json


class StoryTeller:
    """Porivdes a baseline story teller"""

    PROMPT_PATH = "prompts/prompt.json"

    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.environ.get("OPEN_AI_TEST_API_KEY"))

    def weave_story(self, evolutionary_links):
        """Generates a story using the OpenAI API."""
        prompt_messages = self.__format_the_prompt(evolutionary_links)

        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                store=False,
                messages=prompt_messages,
            )
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            raise Exception(f"Failed to generate story: {str(e)}")

        return completion.choices[0].message.content

    def __load_prompt(self):
        try:
            with open(self.PROMPT_PATH, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Error: File '{self.PROMPT_PATH}' not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None

    def __format_the_prompt(self, evolutionary_links):
        json_prompt_data = self.__load_prompt()
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
            {
                "role": "user",
                "content": f"Item {i + 1}: {item['title']}: {item['summary']}",
            }
            for i, item in enumerate(evolutionary_links)
        )
        return messages
