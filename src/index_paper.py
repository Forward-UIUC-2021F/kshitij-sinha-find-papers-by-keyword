from os import read
import pandas as pd
from find_papers_by_keyword.paper_indexer import PaperIndexer
from file_readers.paper_file_reader import PaperFileReader
from find_papers_by_keyword.utils import read_pickle_file
import mysql.connector


def main():
    data_root_dir = 'data/'

    paper_file = data_root_dir + "filtered_arxiv.json"
    golden_keywords_file = data_root_dir + "golden_words.csv"
    keyword_embeddings_file = data_root_dir + "keyword_embs.pickle"
    word_to_other_freq_file = data_root_dir + "other_freqs.pickle"

    paper_reader = PaperFileReader("id", "title", "abstract", None)
    paper_data = paper_reader.read_file(paper_file)

    golden_keywords_full = pd.read_csv(golden_keywords_file)
    golden_keywords = set(golden_keywords_full['word'])

    keyword_embeddings = read_pickle_file(keyword_embeddings_file)
    word_to_other_freq = read_pickle_file(word_to_other_freq_file)

    mydb = mysql.connector.connect(
        host="localhost",
        user="forward",
        password="forward",
        database="assign_1"
    )

    indexer = PaperIndexer(mydb)

    indexer.index_papers(paper_data, golden_keywords, keyword_embeddings, word_to_other_freq,
                         "tmp/paper_embs.pickle", "tmp/paper_id_to_ind.json")


if __name__ == "__main__":
    main()
