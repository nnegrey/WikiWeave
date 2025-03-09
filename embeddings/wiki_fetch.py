"""Wiki Fetch"""

import json
import wikipediaapi


class WikiFetch:

    def __init__(self, lang="en"):
        self.lang = lang
        self.wiki = wikipediaapi.Wikipedia(
            user_agent="WikiWeave (noah.negrey@gmail.com)", language=self.lang
        )

    def print_links(self, page):
        links = page.links
        for title in sorted(links.keys()):
            print("%s: %s" % (title, links[title]))
            linked_page = links[title]
            print(f"\t{linked_page.title}")
            print(f"\t{linked_page.summary}")

    def __add_page_content_to_test_dataset(self, page, pages, _id, truncated_links):
        pages.append(
            {
                "id": _id,
                "title": page.title,
                "title_embedding": None,
                "summary": page.summary,
                "summary_embedding": None,
                "full_url": page.fullurl,
                "canonical_url": page.canonicalurl,
                "linked_titles": truncated_links,
            }
        )

    def create_test_dataset(self):
        start_page = self.wiki.page("Python_(programming_language)")
        pages = []
        visited = set()
        _id = 0
        queue = [start_page]
        while _id < 3 and queue:
            page = queue.pop(0)
            if page.title in visited:
                continue
            visited.add(page.title)

            truncated_links = []
            for i in range(3):
                linked_page = page.links[list(page.links.keys())[i]]
                truncated_links.append({"title": linked_page.title})
                queue.append(linked_page)

            self.__add_page_content_to_test_dataset(page, pages, _id, truncated_links)
            _id += 1

        output_json = {"pages": pages}
        with open("test_dataset.json", "w") as f:
            json.dump(output_json, f)


if __name__ == "__main__":
    wf = WikiFetch()
    wf.create_test_dataset()
