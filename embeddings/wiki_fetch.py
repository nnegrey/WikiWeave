"""Wiki Fetch"""

import json
import wikipediaapi

from embeddings import embedding_generator


class WikiFetch:

    def __init__(self, client, lang="en"):
        self.lang = lang
        self.wiki = wikipediaapi.Wikipedia(
            user_agent="WikiWeave (noah.negrey@gmail.com)", language=self.lang
        )
        self.embed_gen = embedding_generator.EmbeddingGenerator(client)
        # Controls how many links (nodes) in the dataset
        self.num_links_to_traverse = 3
        # Controls how many links (edges) per node in the dataset
        self.num_linked_pages_per_page = 3

    def print_links(self, page):
        links = page.links
        for title in sorted(links.keys()):
            print("%s: %s" % (title, links[title]))
            linked_page = links[title]
            print(f"\t{linked_page.title}")
            print(f"\t{linked_page.summary}")

    def create_test_dataset(self):
        start_page = self.wiki.page("Python_(programming_language)")
        pages = []
        visited = set()
        _id = 0
        queue = [start_page]
        while _id < self.num_links_to_traverse and queue:
            page = queue.pop(0)
            if page.title in visited:
                continue
            visited.add(page.title)

            truncated_links = []
            for i in range(self.num_linked_pages_per_page):
                linked_page = page.links[list(page.links.keys())[i]]
                truncated_links.append({"title": linked_page.title})
                queue.append(linked_page)

            page_as_json = self.__page_to_json(_id, page, truncated_links)

            pages.append(page_as_json)
            _id += 1

        output_json = {"pages": pages}
        with open("knowledge_base/data/dataset.json", "w") as f:
            json.dump(output_json, f)

    def __page_to_json(self, _id, page, truncated_links):
        json_page = {
            "id": _id,
            "title": page.title,
            "title_embedding": None,
            "summary": page.summary,
            "summary_embedding": None,
            "full_url": page.fullurl,
            "canonical_url": page.canonicalurl,
            "linked_titles": truncated_links,
        }
        self.embed_gen.augment_wiki_page_with_generated_embedding(json_page)
        return json_page
