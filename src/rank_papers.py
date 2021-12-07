from utils import gen_sql_in_tup, return_print_err, copy_temporary_table, drop_view, drop_table
import mysql.connector

def store_keywords(keyword_ids, cur, make_copy=True):
    """
    Stores top 10 similar keywords for each input keyword
    Arguments:
    - keyword_ids: list of ids of input keywords
    - cur: db cursor
    Returns: None. each entry in Top_Keywords table is of the form (parent_id, keyword_id, npmi).
    - parent_id: id of the original input keyword
    - keyword_id: id of similar keyword
    - npmi is a similarity score between the two keywords
    Note: the identity row for each keyword_id is included by default with
    similarity score 1 (i.e. for each kw_id in keywords_ids, there will be a
    row in Top_Keywords of (kw_id, kw_id, 1))
    """
    fields_in_sql = gen_sql_in_tup(len(keyword_ids))

    drop_table(cur, "Top_Keywords")
    get_related_keywords_sql = """
        SET @kw_rank := 1, @current_parent := -1;
        
        CREATE TABLE Top_Keywords (
            parent_id INT,
            id INT,
            npmi DOUBLE,
            PRIMARY KEY(parent_id, id)
        )
        SELECT parent_id, id, npmi
        FROM
        (
            SELECT parent_id, id, npmi,
            @kw_rank := IF(@current_parent = parent_id, @kw_rank + 1, 1) AS kw_rank,
            @current_parent := parent_id
            FROM
            (
                (SELECT id2 AS parent_id,
                id1 AS id, npmi
                FROM FoS_npmi_Springer
                WHERE id2 IN """ + fields_in_sql + """)
                UNION
                (SELECT
                id1 AS parent_id,
                id2 as id, npmi
                FROM FoS_npmi_Springer
                WHERE id1 IN """ + fields_in_sql + """)
            ) as top_keywords
            ORDER BY parent_id, npmi DESC
        ) AS ranked_keywords
        WHERE kw_rank <= 10
    """
    get_related_query_params = 2 * keyword_ids
    cur.execute(get_related_keywords_sql, get_related_query_params)


    append_given_sql = """
        INSERT INTO Top_Keywords
        (parent_id, id, npmi)
        VALUES
        """ + ",\n".join(["(%s, %s, 1)"] * len(keyword_ids))

    append_given_query_params = [id for id in keyword_ids for i in range(2)]

    cur.execute(append_given_sql, append_given_query_params)

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