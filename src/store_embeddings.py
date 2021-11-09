import csv
import json
import sys
import argparse
import mysql.connector

from preprocessing.keyword_transformer import KeywordTransformer
from preprocessing.paper_transformer import PaperTransformer
from utils import write_pickle_data


def main():
    """
    Command line program to preprocess keyword and paper files. Will
    generate keyword and paper embeddings and metadata files (in pickle format)

    Script call format:
        python store_embeddings.py --keywords <keyword_file> --papers <paper_file> --out <out_dir>
        <keyword_file> is optional and specifies the csv file of keywords to parse
        <paper_file> is optional and specifies the json file of papers to parse
        <out_dir> is required and specifies the directory to store pickle files in
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--keywords', dest='keyword_file', type=str,
                        help='filepath to csv containing keywords to parse')
    parser.add_argument('--papers', dest='paper_file', type=str,
                        help='filepath to json containing papers to parse')
    parser.add_argument('--out', dest='out_dir', type=str, required=True,
                        help='path to directory where pickle files will be stored')

    args = parser.parse_args()

    mydb = mysql.connector.connect(
        host="localhost",
        user="forward",
        password="forward",
        database="assign_paper_kwds"
    )
    mycursor = mydb.cursor()

    if args.keyword_file != None:
        print(f"Parsing keyword file {args.keyword_file}")
        store_keywords(args.keyword_file, args.out_dir, mycursor)
    if args.paper_file != None:
        print(f"Parsing paper file {args.paper_file}")
        store_papers(args.paper_file, args.out_dir, mycursor)

    mydb.commit()
    mycursor.close()


def store_papers(papers_filepath: str, out_dir: str, cursor):
    """
    Stores the paper embeddings and paper meta into pickle files

    Args:
        paper_filepath: the path to a json file containing papers data
            Json data should be in the following schama:
            [
                {
                    "arxiv_id": "0704.0002",
                    "title": "Sparsity-certifying Graph Decompositions",
                    "abstract": "  We describe a new algorithm, the $(k,\\ell)$-pebble game with colors, and use\nit obtain a characterization of the family of $(k,\\ell)$-sparse graphs and\nalgorithmic solutions to a family of problems concerning tree decompositions of\ngraphs. Special instances of sparse graphs appear in rigidity theory and have\nreceived increased attention in recent years. In particular, our colored\npebbles generalize and strengthen the previous results of Lee and Streinu and\ngive a new proof of the Tutte-Nash-Williams characterization of arboricity. We\nalso present a new decomposition that certifies sparsity based on the\n$(k,\\ell)$-pebble game with colors. Our work also exposes connections between\npebble game algorithms and previous sparse graph algorithms by Gabow, Gabow and\nWestermann and Hendrickson.\n",
                },
                ...
            ]
        out_dir: the directory to store the paper embeddings and metadata pickle files in
    """
    # Output pickle files
    emb_out_file = out_dir + "SB_paper_embeddings.pickle"

    print("Loading paper file")
    with open(papers_filepath) as f:
        paper_ts = json.load(f)

    paper_transformer = PaperTransformer(paper_ts)

    print("Getting embeddings for " + str(len(paper_ts)) + " papers")
    # paper_embeddings = paper_transformer.generateEmbeddings()
    paper_metadata = paper_transformer.getEmbeddingsMetadata()

    print("Done. Saving data")
    # write_pickle_data(paper_embeddings, emb_out_file)
    sql = """
    REPLACE INTO Publication (id, arxiv_id, title, abstract)
    VALUES (%(id)s, %(arxiv_id)s, %(title)s, %(abstract)s)
    """
    cursor.executemany(sql, paper_metadata)



def store_keywords(keywords_filepath: str, out_dir: str, cursor):
    """
    Stores the keywords embeddings and keyword meta into pickle files

    Args:
        keywords_filepath: the path to a csv file containing keywords and frequencies
            csv file should be in the following schema:
                keyword,frequency
        out_dir: the directory to store the keyword embeddings and metadat pickle files in
    """
    # Output pickle files
    emb_out_file = out_dir + "springer_keyword_embs.pickle"

    print("Loading keyword file")
    with open(keywords_filepath, newline='') as f:
        keyword_data_reader = list(csv.DictReader(f, quotechar="|"))

    keyword_transformer = KeywordTransformer(keyword_data_reader)

    print("Getting embeddings for keywords")
    # keyword_embeddings = keyword_transformer.generateEmbeddings()
    keyword_metadata = keyword_transformer.getEmbeddingsMetadata()

    print("Done. Saving data")
    # write_pickle_data(keyword_embeddings, emb_out_file)

    sql = "REPLACE INTO FoS (id, keyword, frequency) VALUES (%(id)s, %(keyword)s, %(frequency)s)"
    cursor.executemany(sql, keyword_metadata)


if __name__ == "__main__":
    main()
