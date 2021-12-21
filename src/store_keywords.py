from src.file_readers.keyword_file_reader import KeywordFileReader
from src.find_papers_by_keyword.database import Database
import mysql.connector
import sql_creds

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="""
            Command-line utility for storing keyword-data into SQL database.
        """
    )
    parser.add_argument('keyword_file', type=str,
                        help='filepath to csv containing keyword data')

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

    db_connection.close()

if __name__ == "__main__":
    main()
