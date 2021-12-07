from file_readers.paper_file_reader import PaperFileReader
from file_readers.keyword_file_reader import KeywordFileReader
import csv
import mysql.connector
import argparse

def main():
    """
    Command line program to preprocess keyword and paper files. Will
    store relevant keyword and paper metadata to MySQL database

    Script call format:
        python store_embeddings.py --keywords <keyword_file> --papers <paper_file> --out <out_dir>
        <keyword_file> is optional and specifies the csv file of keywords to parse
        <paper_file> is optional and specifies the json file of papers to parse
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--keywords', "-k", dest='keyword_file', type=str,
                        help='filepath to csv containing keywords to parse')
    parser.add_argument('--papers', "-p", dest='paper_file', type=str,
                        help='filepath to json containing papers to parse')

    args = parser.parse_args()


    mydb = mysql.connector.connect(
        host="localhost",
        user="forward",
        password="forward",
        database="assign_paper_kwds"
    )
    cursor = mydb.cursor()

    if args.keyword_file != None:
        print(f"Parsing keyword file {args.keyword_file}")
        store_springer_keywords(args.keyword_file, cursor)
    if args.paper_file != None:
        print(f"Parsing paper file {args.paper_file}")
        store_filtered_arxiv(args.paper_file, cursor)

    mydb.commit()
    cursor.close()


def store_springer_keywords(keywords_filepath: str, cursor):
    file_reader = KeywordFileReader("id", "keyword", "frequency")
    
    print("Loading keyword file")

    keyword_data = file_reader.read_file(keywords_filepath)

    print("Saving to table FoS")

    sql = "REPLACE INTO FoS (id, keyword, frequency) VALUES (%(id)s, %(keyword)s, %(frequency)s)"
    cursor.executemany(sql, keyword_data)

def store_filtered_arxiv(papers_filepath: str, cursor):
    file_reader = PaperFileReader("id", "title", "abstract")
    
    print("Loading paper file")

    paper_data = file_reader.read_file(papers_filepath)

    print("Saving to table Publication")

    sql = """
    REPLACE INTO Publication (id, title, abstract)
    VALUES (%(id)s, %(title)s, %(abstract)s)
    """
    cursor.executemany(sql, paper_data)


if __name__ == "__main__":
    main()