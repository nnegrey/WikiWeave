import json


class PromptLoader:
    def __init__(self):
        self.file_path = "prompts/prompt.json"

    def get_prompt(self):
        """Gets a prompt from a JSON file."""
        return self.__load_json_from_file()

    def __load_json_from_file(self):
        """Loads JSON data from a file."""
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
