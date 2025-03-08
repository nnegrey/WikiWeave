from story_teller import prompt_formatter
from prompts import prompt_loader


class SimpleStoryFormatter(prompt_formatter.PromptFormatter):
    def format(self, prompt_args):
        json_prompt_data = prompt_loader.PromptLoader(
            "prompts/prompt.json"
        ).get_prompt()
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
            for i, item in enumerate(prompt_args)
        )
        messages.append({"role": "user", "content": "Start your narrative now."})
        return messages
