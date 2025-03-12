# WikiWeave

Status: Active Development

---

## What is WikiWeave?
* [Design Doc](https://docs.google.com/document/d/144tdxfU6lMPpJtF4ucBPg4v8PdUMpRt4-3NCaa5RU-w/edit?usp=sharing)

WikiWeave is a project for me to get hands on with GenAI and see what kind of project I cant build from an idea → minimum viable product (MVP) → improvements / optimizations and see where that goes.

### The Idea:
Using Wikipedia articles, weave together a evolutionary narrative that tells a story of how we got from article A to article B. The initial idea is to allow for hallucinations and creative storytelling such that you could get a fun story of how Airplanes led to the evolution of Birds (maybe later, I’ll work on the problem of a Factual-WikiWeave that tries to force the correct order, however this is a fun project first).

### Tasks:
1) **Article Identification** - Given a input of two topics: A and B, find the closest related Wikipedia Articles *(A special case of Graph Traversal)*
1) **Graph Traversal** - Create the path (connected graph) between the two articles using the linked articles inside A and B
1) **Story Teller** - Using the context from the article path, create a story for how the first entry led to the second entry

## Component Status

* Dataset
  * Toy dataset for development and testing
  * [**TODO**] Expand the dataset size and get the set of embeddings offline
* Graph Traversal
  * `LinkGenerator` [**alpha**] - Use Prompt Engineering to have the LLM provide links and context which can be used by the StoryTeller
  * `EmbeddingTraversal` [**alpha**]
    * `Article Identification` [**Complete**] - Scans the dataset to find the best matched articles for start and end point.
      * *Optimization* [**TODO**] - Offline process the dataset into layers of Clusters, then continually cluster the input until you have a small enough sample-size to find the best match.
    * [**TODO**] - Traverse the links by selecting the best link from the current node using the target embedding to select the path.
      * *Optimization* [**TODO**] - 
      * *Optimization* [**TODO**] - Cluster the results into smaller groups and create summaries of the clusters to be used by the story teller.
* StoryTeller
  * *SimpleStory* - Creates a fantastical story using the input
  * *Optimization* [**TODO**] - Use the summary text and not just the titles

