"""Link Generator Travesral Strategy"""

from graph_traversal import traversal_strategy
from json_data import json_loader


class LinkGenerator(traversal_strategy.TraversalStrategy):
    """LinkGenerator attempts to use AI to guess what the links would be between the two topics."""

    def __init__(self, openai_client, call_openai=False):
        self.client = openai_client
        self.call_openai = call_openai
        self.json_loader = json_loader.JsonLoader()
        print("\n***** Link Generator Traversal Strategy *****")

    def traverse(
        self,
        start,
        end,
        start_description=None,
        end_description=None,
    ):
        messages = self.__get_prompt_messages(
            start, end, start_description, end_description
        )
        print("Link Generator Prompt Messages:")
        for i, m in enumerate(messages):
            print(f"\t{i}: {m['content']}")

        response = None
        if self.call_openai:
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                store=True,
                messages=messages,
            )

            print(completion.choices[0].message.content)
            response = {"content": completion.choices[0].message.content}
        else:
            response = self.__get_canned_response()
        # TODO: Parse the response better to get the links and the descriptions
        # TODO: Improve the prompt to get the output in the format I want
        return [start] + response["content"].split(",") + [end]

    def __get_prompt_messages(
        self, start, end, start_description=None, end_description=None
    ):
        json_prompt_data = self.json_loader.get_json(
            "json_data/prompts/link_gen_3.json"
        )
        messages = [
            {
                "role": "system",
                "content": f"{json_prompt_data['task_content']}. "
                + f"{json_prompt_data['task_example']}. "
                + f"{json_prompt_data['output_format']}. "
                + f"{json_prompt_data['start_task']} {start}."
                + f"{json_prompt_data['end_task']} {end}. "
                + f"{json_prompt_data['chain_of_reasoning']} ",
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

    def __get_canned_response(self):
        """Skip calls to OpenAI for faster development."""
        return self.json_loader.get_json(
            "json_data/sample_output/open_ai_link_gen_response.json"
        )
