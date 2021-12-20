from find_papers_by_keyword.paper_indexer import PaperIndexer
from file_readers.paper_file_reader import PaperFileReader
import mysql.connector

def main():
    paper_file = "test_data/papers.json"

    paper_reader = PaperFileReader("id", "title", "abstract", None)
    paper_data = paper_reader.read_file(paper_file)

    mydb = mysql.connector.connect(
        host="localhost",
        user="forward",
        password="forward",
        database="assign_1"
    )

    indexer = PaperIndexer(mydb)

    indexer.index_papers(paper_data, "tmp/paper_embs.pickle", "paper_id_to_ind.json")



if __name__ == "__main__":
    main()