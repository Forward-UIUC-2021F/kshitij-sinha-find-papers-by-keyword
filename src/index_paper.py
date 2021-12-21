import pandas as pd
from find_papers_by_keyword.paper_indexer import PaperIndexer
from file_readers.paper_file_reader import PaperFileReader
from file_readers.keyword_file_reader import KeywordFileReader
from find_papers_by_keyword.utils import read_pickle_file, read_json_file
import mysql.connector

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="""
            Command-line utility for loading paper-data for searching.
            First, the paper data is stored to the Publication table.
            Then, keywords are assigned to every paper and stored in the Publication_FoS table.

            The second task requires computing paper embeddings and a mapping from paper ids to the
            row index of the paper's embedding in the embedding matrix. There are two options to do this.
            
            1)  Let the utility compute the embeddings and mapping and store them to a file. To use this
                option, supply the optional arguments --papers_embs_in and --paper_id_to_embs_in, specifying
                the file to store the data in
            2)  Precompute the embeddings and mapping and direct the utility to skip the computation. To use
                this option, supply the optional arguments --papers_embs_out and --paper_id_to_embs_out, specifying
                the location of the data
        """
    )
    parser.add_argument('papers_file', type=str,
                        help='filepath to json containing paper data')
    parser.add_argument('golden_keywords_file', type=str,
                        help='filepath to csv containing golden keywords data')
    parser.add_argument('keyword_embeddings_file', type=str,
                        help='filepath to json containing paper data')
    parser.add_argument('word_to_other_freq_file', type=str,
                        help='filepath to pickle mapping words to non-CS frequences')

    # For paper embeddings, either take in-argument for precomputed embeddings
    # or out-argument to compute and save embeddings
    parser.add_argument('--paper_embs_in', dest='paper_embeddings_file_in', type=str,
                        help='filepath to pickle containing paper embeddings')
    parser.add_argument('--paper_mapping_in', dest='paper_id_to_embs_file_in', type=str,
                        help='filepath to json mapping paper ids to embedding-matrix rows')
    parser.add_argument('--paper_embs_out', dest='paper_embeddings_file_out', type=str,
                        help='filepath to save pickle containing paper embeddings')
    parser.add_argument('--paper_mapping_out', dest='paper_id_to_embs_file_out', type=str,
                        help='filepath to save json mapping paper ids to embedding-matrix rows')

    args = parser.parse_args()

    load_embeddings = args.paper_embeddings_file_in != None and args.paper_id_to_embs_file_in != None
    store_embeddings = args.paper_embeddings_file_out != None and args.paper_id_to_embs_file_out != None

    if (not load_embeddings) and (not store_embeddings):
        print(
            "Error: Please enter either in-arguments or out-arguments for paper embeddings")
        return

    print("Loading and parsing files...")
    paper_reader = PaperFileReader("id", "title", "abstract", None)
    paper_data = paper_reader.read_file(args.papers_file)[:10]

    golden_keywords_full = pd.read_csv(args.golden_keywords_file)
    golden_keywords = set(golden_keywords_full['word'])

    keyword_embeddings = read_pickle_file(args.keyword_embeddings_file)
    word_to_other_freq = read_pickle_file(args.word_to_other_freq_file)

    print("Connecting to database...")
    mydb = mysql.connector.connect(
        host="localhost",
        user="forward",
        password="forward",
        database="assign_1"
    )

    indexer = PaperIndexer(mydb)

    print("Indexing papers...")
    if load_embeddings:
        paper_embeddings = read_pickle_file(args.paper_embeddings_file_in)
        paper_id_to_embs = read_json_file(args.paper_id_to_embs_file_in)
        indexer.index_papers_with_embs(paper_data, golden_keywords, paper_embeddings,
                                       keyword_embeddings, paper_id_to_embs, word_to_other_freq)
    elif store_embeddings:
        indexer.index_papers(paper_data, golden_keywords, keyword_embeddings, word_to_other_freq,
                             args.paper_embeddings_file_out, args.paper_id_to_embs_file_out)

    print("Paper indexing complete")

if __name__ == "__main__":
    main()
