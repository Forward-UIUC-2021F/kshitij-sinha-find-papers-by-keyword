from src.file_readers.keyword_file_reader import KeywordFileReader
from src.find_papers_by_keyword.database import Database
from src.find_papers_by_keyword.embeddings_generator import EmbeddingsGenerator
from src.find_papers_by_keyword.utils import write_pickle_data
import mysql.connector
import sql_creds

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="""
            Command-line utility for storing keyword-data into SQL database.

            Takes keyword data in the form of a CSV and saves the
            data to the MySQL database. Also generates keyword embeddings as saves
            them to a pickle file
        """
    )
    parser.add_argument('keyword_file', type=str,
                        help='filepath to csv containing keyword data')
    parser.add_argument('keyword_embs_outfile', type=str,
                        help='filepath specifying destiation of keyword embeddings pickle file')

    args = parser.parse_args()
    print("Loading and parsing files...")
    keyword_reader = KeywordFileReader("id", "keyword", "frequency")
    keyword_data = keyword_reader.read_file(args.keyword_file)

    db_connection = mysql.connector.connect(
        host=sql_creds.db_host,
        user=sql_creds.db_user,
        password=sql_creds.db_password,
        database=sql_creds.db_name
    )

    database = Database(db_connection)
    database.store_keyword_data(keyword_data)

    embeddings_generator = EmbeddingsGenerator()
    keyword_embs = embeddings_generator.generate_keyword_embeddings(keyword_data)

    write_pickle_data(keyword_embs)

    db_connection.close()

if __name__ == "__main__":
    main()
