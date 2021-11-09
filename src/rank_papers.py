import mysql.connector



def rank_papers_keyword(keyword, cur):
    # Aggregate scores for each author
    get_author_ranks_sql = """
        SELECT Publication.title, Publication.arxiv_id FROM Publication_FoS
        LEFT JOIN Publication
        ON Publication_FoS.Publication_id = Publication.id
        LEFT JOIN FoS
        ON Publication_FoS.FoS_id = FoS.id
        WHERE FoS.keyword=%s
        ORDER BY score DESC;
    """
    cur.execute(get_author_ranks_sql, (keyword, ))
    author_ranks = cur.fetchall()

    # res = [{
    #     'id': t[0],
    #     'name': t[1],
    #     'score': t[2]
    # } for t in author_ranks]

    # top_author_ids = [t["id"] for t in res]

    # author_id_to_idx = {}
    # for i in range(len(top_author_ids)):
    #     author_id = top_author_ids[i]
    #     author_id_to_idx[author_id] = i

    return author_ranks




if __name__ == '__main__':

    # Setting up db
    db = mysql.connector.connect(
      host="localhost",
      user="forward",
      password="forward",
      database="assign_paper_kwds"
    )
    cur = db.cursor()

    top_authors = rank_papers_keyword("polynomial time", cur)
    print(*top_authors, sep="\n")

    cur.close()