"""Storage Layer for the Wiki Dataset"""

from json_data import json_loader


class StorageLayer:
    """The Storage Layer is the interface for the JSON WikiWeave Dataset

    For now it is simply a JSON file with a test dataset, however I hope to add a real database /
    vector embedding database to store the data in the future. But I think it will always return
    the data in the same JSON format.
    """

    def __init__(self):
        self.json_dataset = json_loader.JsonLoader().get_json(
            "knowledge_base/dataset.json"
        )

    def find_start_and_end_nodes(self, start_embedding_input, end_embedding_input):
        """Find most relevant entries in DB with embeddings based on title, I don't like having
        logic in my storage layer, but I have to come up with a better solution later.

        Returns a tuple of the start and end nodes
        """
        pass

    # TODO: Probably switch this to id later and store the list of ids instead of titles
    # Optimizations:
    # - return only the summary_embedding
    # - fetch all linked_pages at once
    def get_node(self, title):
        """Get a node from the dataset by title"""
        for page in self.json_dataset["pages"]:
            if page["title"] == title:
                return page
        return None
