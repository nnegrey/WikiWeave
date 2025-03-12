"""Quck one-off to modify the dataset to the format I want going forward"""

import json
import pandas as pd
import csv


def get_json(file_path):
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


json_dataset = get_json("dataset.json")
pages_json = []
links_json = []
embeddings_json = []
for page in json_dataset["pages"]:
    pages_json.append(
        {
            "id": page["id"],
            "title": page["title"],
            "summary": page["summary"].replace("\n", "\\n"),
            "full_url": page["full_url"],
            "canonical_url": page["canonical_url"],
        }
    )
    links = []
    for link in page["linked_titles"]:
        links.append(link["title"])
    links_json.append(
        {
            "id": page["id"],
            "linked_titles": links,
        }
    )
    embeddings_json.append(
        {
            "id": page["id"],
            "title_embedding": page["title_embedding"],
            "summary_embedding": page["summary_embedding"],
        }
    )
pages_df = pd.DataFrame(pd.json_normalize(pages_json))
links_df = pd.DataFrame(pd.json_normalize(links_json))
embeddings_df = pd.DataFrame(pd.json_normalize(embeddings_json))
pages_df.to_csv("data/pages.csv", index=False, quoting=csv.QUOTE_ALL)
links_df.to_csv("data/links.csv", index=False, quoting=csv.QUOTE_ALL)
embeddings_df.to_csv("data/embeddings.csv", index=False, quoting=csv.QUOTE_ALL)

print(pages_df)
print(links_df)
print(embeddings_df)
