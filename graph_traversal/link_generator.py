"""Link Generator Travesral Strategy"""

import os
from dotenv import load_dotenv
from openai import OpenAI

from graph_traversal import traversal_strategy
from prompts import prompt_loader


class LinkGenerator(traversal_strategy.TraversalStrategy):
    """LinkGenerator attempts to use AI to guess what the links would be between the two topics."""

    def __init__(self):
        """Load environment variables from .env file and initialize the OpenAI client."""
        load_dotenv()
        self.client = OpenAI(api_key=os.environ.get("OPEN_AI_TEST_API_KEY"))
        self.json_prompt_data = prompt_loader.PromptLoader(
            "prompts/link_gen_3.json"
        ).get_prompt()

    def __get_prompt_messages(
        self, start, end, start_description=None, end_description=None
    ):
        messages = [
            {
                "role": "system",
                "content": f"{self.json_prompt_data['task_content']}. "
                + f"{self.json_prompt_data['task_example']}. "
                + f"{self.json_prompt_data['output_format']}. "
                + f"{self.json_prompt_data['start_task']} {start}."
                + f"{self.json_prompt_data['end_task']} {end}. "
                + f"{self.json_prompt_data['chain_of_reasoning']} ",
            },
        ]
        if start_description:
            messages.append(
                {
                    "role": "system",
                    "content": f"Here is additional information about {start}: {start_description}",
                }
            )
        if end_description:
            messages.append(
                {
                    "role": "system",
                    "content": f"Here is additional information about {start}: {start_description}",
                }
            )
        return messages

    def traverse(
        self,
        start,
        end,
        call_openai=False,
        start_description=None,
        end_description=None,
    ):
        messages = self.__get_prompt_messages(
            start, end, start_description, end_description
        )
        print(messages)
        if call_openai:
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                store=True,
                messages=messages,
            )

            print(completion.choices[0].message)
            return completion.choices[0].message
        else:
            return [start, "t1", "t2", "t3", end]
