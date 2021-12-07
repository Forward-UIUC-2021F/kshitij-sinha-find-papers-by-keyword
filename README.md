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
Given a dataset of research papers and popular computer-science-related keywords, we can generate embeddings for research papers (a combination of title and abstract), and individual keywords using Python `Sentence Transformers`. With these embeddings, we can use a similarity function like Cosine Similarity to compute a score for each pair of keyword-paper matches. We can filter out duplicate keywords using a clustering algorithm on the keyword embeddings. The resulting data gives us the top _n_ keywords present in any research paper. This data can be stored in a SQL table. At its simplest, every row in the table will contain a paper id and a keyword id.

To retrieve a list of papers given a search query of keywords, we can do a SQL lookup on our above table. We will filter all rows that contain the input keywords and collect the the corresponding papers.

The algorithm will be split into three sections: Generate paper embeddings, assign papers to keywords, find papers by keywords.

The overall architecture of this module is outlined in the diagram below.
![System Context](/figures/SystemContext.png)

### 1: Generate Embeddings
In this step, we will create a vector embedding for every paper on our dataset. This will be done through the Python library `Sentence Transformers`. For every paper, we will concatenate the paper title and abstract, and use this string to genereate a vector embedding. We will do the same for every keyword.
![Generate Embeddings](/figures/1_GenerateEmbeddings.png)

### 2: Assign To Keywords
![Generate Embeddings](/figures/2_AssignPaperKeywords.png)
Every paper is then assigned a set of keywords that best describe the keywords contents. The algorithm to assign top keywords to papers is described here.

1) Create a regex-based keyword-search index to quickly search for mathing keywords. This regex index will be constructed through an intermediary prefix trie. (implementation found in `src/trie/Trie.py`). We call this index `keywords_re`.

2) Iterate through every paper, `paper_i`, defining  `pt_i` to be the concatenation of the paper title and abstract. 
  
    1) Using `keywords_re`, find all keywords that occur in `pt_i`, and iterate through every matching keyword, 'match_kwd` 
    
        1) Compute the Cosine Similarity between the embeddings corresponding to `pt_i` and the `match_kwd` and store the result as `match_score`.
        2) Our search service will primarily receive keywords relating to the field of computer science. Therefore, we want to prioritize CS-focused keywords in our assignment algorithm. To do this, we penalize keywords that appear frequently in non-CS papers. We do this by dividing `match_score` by its squre root: 
        
            ```match_score /= sqrt(match_score)```
    2) Keep the 9 _unique_ keywords with the highest match scores. To do so, we first we then use DBSCAN clustering on the our keyword matches. If any subset of keywords fall into the same cluster, we keep only one of the keywords. Once we've filtered out "duplicate" keywords, we select the top 9 of our remaining keywords.
    3) For each of the 9 keywords, `unique_kwd` and its corresponding match score, `match_score`, store the entry `(paper_i, unique_kwd, match_score)` in a MySQL Table called `Publication_FoS`.

### 3: Find papers by Keywords
![Generate Embeddings](/figures/3_FindPapers.png)
The goal of this step is receive a set of query keywords and output a list of research papers that best match the query keywords. We do this by computing a `rank_score` for each paper using data computed from previous stages of this module.

1) Initially, we receive a set of `n` keywords `k_1...k_n`
2) For any _parent_ keyword `k_i`, we find the top-10 _similar_ keywords `sk_i,1 sk_i,10` using precomputed Normalized-PMI (NPMI) scores. We do this for every keyword and store the list of similar keywords `sk_0,0...sk_n,10`. We also store the NPMI score between the every _parent_ keyword `k_i` and _similar_ keyword `sk_i,j`, storing these scores in a list: `npmi_0,0...npmi_n,10`.
3) For every similar keyword `sk_i,j`, we find all the research papers from `Publication_FoS`, `p_k` and it's corresponding Cosine Similarity match score `cs_k`. Every paper also has a corresponding citation count `cit_k`.
4) We finally compute the rank score for paper `p` like so.


![Generate Embeddings](/figures/rank_scores.png)