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
