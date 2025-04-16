"""WikiWeave Main"""

from story_teller import story_teller
from graph_traversal import graph_traversal
from knowledge_base import storage_layer


class WikiWeave:
    """Entry point to running WikiWeave"""

    def __init__(self, client):
        self.client = client
        self.storage_layer = storage_layer.StorageLayer()

    def weave(self, args):
        """Weaves an evolutionary tale given the input and selected configuration"""
        print(
            f"Finding the linked path between the two items: {args.start_item}, {args.end_item}\n"
        )
        items = graph_traversal.GraphTraversal(
            args.graph_traversal, self.client, self.storage_layer, args.call_openai
        ).find_linked_path(args.start_item, args.end_item)

        if len(items) < 10:
            return

        # print(f"\nLinked Items: {items}\n")
        print("\nWeaving the story...")
        story_teller.StoryTeller(args.story_teller).generate_story(
            items, args.call_openai
        )
