from find_papers_by_keyword.rank_papers import PaperSearchEngine
from find_papers_by_keyword.database import Database
import mysql.connector
import argparse


def build_result_string(rank, title, abstract, match_score):
    return f'Paper {rank}\n' + \
        f'Score: {match_score}\n' + \
        f'Title: {title}\n' + \
        f'Abstract: {abstract}\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('keywords', type=str, nargs='+',
                        help='keywords in search query. Separate with spaces')
    args = parser.parse_args()

    db_connection = mysql.connector.connect(
        host="localhost",
        user="forward",
        password="forward",
        database="assign_paper_kwds"
    )
    database = Database(db_connection)

    engine = PaperSearchEngine(db_connection)
    search_results = engine.get_relevant_papers(
        args.keywords, 15)

    ids = tuple(res[0] for res in search_results)
    papers = database.get_paper_data_by_id(ids)
    rank = 1
    for paper, result in zip(papers, search_results):
        title = paper['title']
        abstract = paper['abstract']
        id, match_score = result

        print(
            f'Paper {rank}:\tID: {id}\n' + \
            f'Score: {match_score}\n' + \
            f'Title: {title}\n' + \
            f'Abstract: {abstract}\n'
        )
        rank += 1


if __name__ == "__main__":
    main()
