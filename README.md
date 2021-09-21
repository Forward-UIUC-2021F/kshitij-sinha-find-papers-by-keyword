# find-papers-by-keyword

This module is responsible for finding research papers that are most relevant to a set of query keywords. The list of papers should be ranked by their relavance to the keywords.

## Functional Design
* Finds the top `n` papers that match a set of query keywords and returns them as a list, sorted in descending order by match scores.
```python
get_relevant_papers(keywords):
  ...
  return [(paper_1_id, match_1_score), (paper_2_id, match_2_score), ..., (paper_n_id, match_n_score)]
```
* Computes and returns the match summary information between a specific research paper and keyword. The match summary will describe how the keywords match the paper and which keywords are most releavant to the paper
```python
compute_match_score(paper_id, keyword):
  ...
  return match_score
```

## Algorithmic Design
For now, I propose a similar solution to that presented in a past FORWARD project used to rank researchers by keyword. The source of the data is still TBD.

Given a dataset of research papers and popular computer-science-related keywords, we can generate embeddings for research papers (a combination of title and abstract), and individual keywords using Python `Sentence Transformers`. With these embeddings, we can use a similarity function like Cosine Similarity to compute a score for each pair of keyword-paper matches. We can filter out duplicate keywords using a clustering algorithm on the keyword embeddings. The resulting data gives us the top _n_ keywords present in any research paper. This data can be stored in a SQL table. At its simplest, every row in the table will contain a paper id and a keyword id.

To retrieve a list of papers given a search query of keywords, we can do a SQL lookup on our above table. We will filter all rows that contain the input keywords and collect the the corresponding papers.
