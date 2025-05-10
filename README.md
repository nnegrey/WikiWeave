# WikiWeave

Status: Working Prototype
Next: Deploy the Prototype

---

## What is WikiWeave?
* [Design Doc](https://docs.google.com/document/d/144tdxfU6lMPpJtF4ucBPg4v8PdUMpRt4-3NCaa5RU-w/edit?usp=sharing)

WikiWeave is a fun project which uses the SimpleWiki dataset, embeddings, and GenAi to weave a
evolutionary story between two articles and the linked path that story must take.

Using Wikipedia articles (SimpleWiki), weave together a evolutionary narrative that tells a story of how we got from article A to article B. The initial idea is to allow for hallucinations and creative storytelling such that you could get a fun story of how Airplanes led to the evolution of Birds

### Tasks:
1) **Article Start/End** - Randomly select two articles from the dataset.
1) **Graph Traversal** - Create the path (connected graph) between the two articles using the linked articles inside A and B using the embeddings of the articles to choose the path.
1) **Story Teller** - Using the context from the article path, create a story for how the first entry led to the second entry

## Component Status

* Dataset Sources
  * [SimpleWiki](https://dumps.wikimedia.org/simplewiki/) - [Database layout](https://www.mediawiki.org/wiki/Manual:Database_layout)
    * **[page](https://www.mediawiki.org/wiki/Manual:Page_table)**
      * page_id
      * page_title
      * page_namespace
      * page_is_redirect
      * page_random
    * **[pagelinks](https://www.mediawiki.org/wiki/Manual:Pagelinks_table)**
      * pl_target_id
      * pl_from
    * **[linktarget](https://www.mediawiki.org/wiki/Manual:Linktarget_table)**
      * lt_id
      * lt_title
  * [Wikipedia-simple-openai-embeddings](https://www.kaggle.com/datasets/stephanst/wikipedia-simple-openai-embeddings)
    * **page_embeddings**
      * title
      * content
      * embedding
* Graph Traversal
  * `EmbeddingTraversal` [**Working Prototype**]
    * [**Working Prototype**] - Traverse the links from both the start / target articles using the embeddings to choose th best linked article, then update the "start" / "target" articles to the selected linked articles and continue until a path is found.
      * *Optimization* [**TODO**] - Cluster the results into smaller groups and create summaries of the clusters to be used by the story teller.
* StoryTeller
  * *SimpleStory* - Creates a evolutionary linked story using the input links to go from the start to the end

