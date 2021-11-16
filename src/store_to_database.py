import csv
import json
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
        <out_dir> is required and specifies the directory to store pickle files in
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--keywords', "-k", dest='keyword_file', type=str,
                        help='filepath to csv containing keywords to parse')
    parser.add_argument('--papers', "-p", dest='paper_file', type=str,
                        help='filepath to json containing papers to parse')
    parser.add_argument('--out', "-o", dest='out_dir', type=str, required=True,
                        help='path to directory where pickle files will be stored')

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
    print("Loading keyword file")
    with open(keywords_filepath, newline='') as f:
        keyword_data = list(csv.DictReader(f, quotechar="|"))

    metadata = []

    for ind, keyword_entry in enumerate(keyword_data):
        metadata.append({
            "keyword": keyword_entry['keyword'],
            "id": ind,
            "frequency": keyword_entry["frequency"],
        })

    print("Saving to table FoS")

    sql = "REPLACE INTO FoS (id, keyword, frequency) VALUES (%(id)s, %(keyword)s, %(frequency)s)"
    cursor.executemany(sql, metadata)

def store_filtered_arxiv(papers_filepath: str, cursor):
    print("Loading paper file")
    with open(papers_filepath) as f:
        paper_json = json.load(f)

    metadata = []

    for ind, paper in enumerate(paper_json):
        entry = {
            'id': ind,
            'arxiv_id': paper['id'],
            'title': paper['title'],
            'abstract': paper['abstract'],
        }
        metadata.append(entry)

    print("Saving to table Publication")
    
    sql = """
    REPLACE INTO Publication (id, arxiv_id, title, abstract)
    VALUES (%(id)s, %(arxiv_id)s, %(title)s, %(abstract)s)
    """
    cursor.executemany(sql, metadata)


if __name__ == "__main__":
    main()