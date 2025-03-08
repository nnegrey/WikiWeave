import json


class JsonLoader:
    def get_json(self, file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
