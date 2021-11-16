import mysql.connector

from sentence_transformers import SentenceTransformer
from utils import write_pickle_data, concat_paper_info


def main():
    """
    Command line program to generate keyword and paper embeddings, where data is
    accessed from a database
    """

    mydb = mysql.connector.connect(
        host="localhost",
        user="forward",
        password="forward",
        database="assign_paper_kwds"
    )
    dictcursor = mydb.cursor(dictionary=True)

    dictcursor.execute("""
        SELECT keyword
        FROM FoS
    """)
    keywords = dictcursor.fetchall()


    dictcursor.execute("""
        SELECT id, title, abstract
        FROM Publication
    """)
    paper_text = dictcursor.fetchall()

    store_keyword_embeddings(keywords, "springer_keyword_embs.pickle")
    store_paper_embeddings(paper_text, "SB_paper_embeddings.pickle")

    mydb.commit()
    dictcursor.close()


def store_paper_embeddings(paper_data: dict, out_file: str):
    """
    Stores the paper embeddings and paper meta into pickle files

    Args:
        paper_data: dictionary containing paper title and abstract, using the folloing schema:
            [
                {
                    "title": "Sparsity-certifying Graph Decompositions",
                    "abstract": "  We describe a new algorithm, the $(k,\\ell)$-pebble game ..."
                },
                ...
            ]
        out_file: the file to store the paper embeddings in
    """
    print("Getting embeddings for " + str(len(paper_data)) + " papers")

    model = SentenceTransformer('bert-base-nli-mean-tokens')
    paper_raw = [concat_paper_info(t['title'], t['abstract']) for t in paper_data]

    paper_embeddings = model.encode(paper_raw, show_progress_bar=True)

    print("Done. Saving data")
    write_pickle_data(paper_embeddings, out_file)



def store_keyword_embeddings(keyword_data: str, out_file):
    """
    Stores the keywords embeddings and keyword meta into pickle files

    Args:
        keywords_data: dictionary of keywords, using the following schema:
            [
                {
                    "keyword": "machine learning",
                },
                {
                    "keyword": "deep learning",
                }
                ...
            ]
        out_dir: the directory to store the keyword embeddings and metadat pickle files in
    """
    print("Getting embeddings for keywords")

    model = SentenceTransformer('bert-base-nli-mean-tokens')
    keywords = [d['keyword'] for d in keyword_data]
    keyword_embeddings = model.encode(keywords, show_progress_bar=True)

    print("Done. Saving data")
    write_pickle_data(keyword_embeddings, out_file)


if __name__ == "__main__":
    main()
