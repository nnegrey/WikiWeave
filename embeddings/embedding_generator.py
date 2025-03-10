"""Embedding Generator for the Storage Layer"""

import os
from dotenv import load_dotenv
from openai import OpenAI


class EmbeddingGenerator:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.environ.get("OPEN_AI_TEST_API_KEY"))
        self.embedding_model = "text-embedding-3-small"
        # Explicitly set dimension size to 256, because we are starting with summary text only
        # (Plus keep costs down, if I get to it later, I'd love to do a performance comparison)
        # Embed the Title
        self.num_dimensions = 256

    def augment_wiki_page_with_generated_embedding(self, wiki_page_json):
        """Augment the Wiki Page with the embedding data for the title and summary."""
        response = self.client.embeddings.create(
            input=wiki_page_json["title"],
            model=self.embedding_model,
            dimensions=self.num_dimensions,
        )
        wiki_page_json["title_embedding"] = response.data[0].embedding
        # Embed the Summary
        response = self.client.embeddings.create(
            input=wiki_page_json["summary"],
            model=self.embedding_model,
            dimensions=self.num_dimensions,
        )
        wiki_page_json["summary_embedding"] = response.data[0].embedding
