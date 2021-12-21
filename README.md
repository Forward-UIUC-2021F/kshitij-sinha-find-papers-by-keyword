# find-papers-by-keyword

This module is responsible for finding research papers that are most relevant to a set of query keywords. The list of papers should be ranked by their relavance to the keywords.

## Setup
1) Install necessary module dependencies
```
pip install -r requirements
```
2) Download `drive_data.zip` from [Forward Shared Data Drive](https://drive.google.com/drive/u/1/folders/1vq72EBXH38lb7qJbJsBIkHZiOW35NByI). Uncompress the zip file into a folder named `data/`
3) This module uses MySQL to query paper data. Install MySQL using the [MySQL Installation Guide](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)
4) Create an empty MySQL database
5) Populate the database using the `dump.sql` file in the `data/` folder
```
mysql -u [user] -p [database_name] < data/dump.sql
```

To find papers by keyword, use this module either as command-line utility or a library
### Using as a command-line utility
1) Replace contants in`src/sql_creds.py` with your database credentials.
2) We will use `src/find_papers.py` to find papers by keyword. Run the script using the following command
    ```
    python src/find_papers.py [list of keywords]
    ```
    Where `[list of keywords]` is a space-delimited list of keywords in the search query.
    For example, we can find all papers related to "machine learning" and "genetic algorithms" using the following command
    ```
    python src/find_papers.py "machine learning" "genetic algorithms"
    ```

### Using as a library
The `src/find_papers_by_keyword` package contains all the Classes and Methods used to search for papers. Specifically, we use the PaperSearchEngine class in `src/find_papers_by_keyword/paper_search_engine.py`

1) Create a database connection using mysql.connector
```
db = mysql.connector.connect(host, user, password, database)
```
2) Create an instance of PaperSearchEngine using the new database connection
```
search_engine = PaperSearchEngine(db)
```
3) Search for papers using the `get_relevant_papers` method. See **Functional Design** for more information
```
results = search_engine.get_relevant_papers(("machine learning", "genetic algorithmns"), 15)
```
`results` will be a list of tuples of relevant paper data and the corresponding match score.

## Changing Paper Search Space
The `dump.sql` comes with all the intermediate data necessary to search by keywords through the Arxiv dataset. To be able to search through a set of different papers, we need to store the new paper data and do intermediate processing.

1) **Optionally** delete all rows in the `Publication` and `Publication_FoS` table in the MySQL database. Only do this if you want to search exclusively through the new set of of paper data.
3) Download a paper dataset. See `mag_papers` zip files in [OAG Dataset](https://www.microsoft.com/en-us/research/project/open-academic-graph/) for an example.
To work with the module, the paper data must be a `json` file in the following format. Do any preprocessing necessary to convert the data to this format.
```
[
    {
        "id": str,
        "title": str,
        "abstract": str,
        "citations": int,
        ...
    },
    ...
]
```
2) Create a `MySQL.connector.MySQLConnection`
3) In a Python program, create an instance of `PaperIndexer`, found in `src/find_papers_by_keyword/paper_indexer.py`.
5) We will run the `index_papers` method in `PaperIndex`. Load the processed paper data, golden keywords data (`data/golden_keywords.csv`), keword embeddings data (`data/keyword_embs.pickle`), keyword frequency on non-CS paper data (`data/other_freqs.pickle`) into a Python program, according to the schemas outlined in the method docstring.
6) Call the `index_papers` method using the loaded data. The method will save the new paper data into  _Note: the method optionally takes two additional arguments to store the computed paper embeddings in pickle files_

For an example of how this works, see the command-line utility `store_papers.py`

## Testing
This module contains a test suite to verify the functionality of the components. The tests are located in the `test` directory.

* To run all tests, use the following command from the root directory, `kshitij-sinha-find-papers-by-keyword`
    ```
    python -m unittest discover
    ```

* To run all tests in a specific Python module, use the command
    ```
    python -m unittests [path to test module]
    ```
    Where `path to test module` is a dot-delimited path from the root directory to the test module.
    For example, to run the tests in `test/find_papers_by_keyword/test_assign_paper_keywords.py`, run
    ```
    python -m test.find_papers_by_keyword.test_assign_paper_keywords
    ```
    
 _Note that the tests in `test_rank_papers.py` only work with data from the `dump.sql` file_

## Project Structure
```
kshitij-sinha-find-papers-by-keyword/
  - database_setup/create_tables.sql
  - scripts/
  - src/
    - find_papers.py
    - store_papers.py
    - find_paper_by_keyword/
      - assign_paper_keywords.py
      - database.py
      - embeddings_generator.py
      - paper_indexer.py
      - rank_papers.py
      - utils.py
    - fild_readers/
      - keyword_file_reader.py
      - paper_file_reader.py
  - test/
  - test_data/
```
* `database_setup/create_tables.sql`: Contains definitions of SQL tables required for the module to operate
* `scripts/`: Contains small scripts used generate test data and to process data files to conform to the schema required by the module.
* `src/`: Contains all module source code, including command-line utilities for demonstration purposes
  * `src/find_papers.py`: CLI utility to demonstrate how keywords are used to search for papers
  * `src/store_papres.py`: CLI utility to demonstrate how embeddings are generated and how keywords are assigned to papers
  * `src/find_paper_by_keyword/`: The primary package of this module. This package is designed to work by itself and contains all the functions outlines in the **Functional Design**
  * `src/file_readers/`: Contains Python Classes to read paper and keyword. These Classes are only used by the scripts in `src/`
* `test/`: Contains test code. Reflects the structure of `src/`
* `test_data/`: Contains data used in test suite


## Functional Design
### PaperSearchEngine
* Finds the top `n` papers that match a set of query keywords and returns them as a list, sorted in descending order by match scores.
```python
get_relevant_papers(keywords, search_limit):
  ...
  return [(paper_1_id, match_1_score), (paper_2_id, match_2_score), ..., (paper_n_id, match_n_score)]
```
* Computes and returns the match summary information between a specific research paper and keyword. The match summary will describe how the keywords match the paper and which keywords are most releavant to the paper
```python
compute_match_score(paper_id, keyword):
  ...
  return match_score
```
### PaperIndexer
* Stores paper data to the database. Computes embeddings using the paper contents and compares with keyword embeddings to find the top keywords (from `golden_keywords`) that match every paper. Stores these paper-keyword assignments and the corresponding similarity scores to the database. Penalizes any keyword that appears frequently in non-CS papers.
```python
get_relevant_papers(paper_data, golden_keywords, keyword_embeddings, word_to_other_freq):
  ...
  return None
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
4) We finally compute the rank score for paper `p_k` like so.


![Generate Embeddings](/figures/rank_score.png)
