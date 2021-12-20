import mysql.connector 

class Database():
    def __init__(self, db):
        self.db = db

    def get_keyword_data(self) -> dict:
        with self.db.cursor(dictionary=True) as dictcursor:
            dictcursor.execute("""
                SELECT keyword
                FROM FoS
            """)
            return dictcursor.fetchall()

    def get_paper_data(self) -> dict:
        with self.db.cursor(dictionary=True) as dictcursor:
            dictcursor.execute("""
                SELECT id, title, abstract
                FROM Publication Publication
            """)
            return dictcursor.fetchall()

    def store_paper_data(self, paper_data) -> None:
        """
        Stores paper_data as rows in database

        Args:
            paper_data: list of dictionaries containing paper data, using the folloing schema:
                [
                    {
                        "id": str
                        "title": str
                        "abstract": str
                        "citations": int
                    },
                    ...
                ]
        """

        sql = """
        REPLACE INTO Publication (id, title, abstract, citations)
        VALUES (%(id)s, %(title)s, %(abstract)s, %(citations)s)
        """

        with self.db.cursor() as cursor:
            cursor.executemany(sql, paper_data)

        self.db.commit()

    def store_keyword_data(self, keyword_data) -> None:
        """
        Stores keyword_data as rows in database
        
        Args:
            keyword_data: list of dictionaries containing keyword data, using the following schema:
                [
                    {
                        "id": str
                        "keyword": str
                        "frequency" : int
                    },
                    ...
                ]
        """

        sql = "REPLACE INTO FoS (id, keyword, frequency) VALUES (%(id)s, %(keyword)s, %(frequency)s)"
        with self.db.cursor() as cursor:
            cursor.executemany(sql, keyword_data)

        self.db.commit()