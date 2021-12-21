import mysql.connector

class Database():
    """ Provides methods to write and read from a MySQL database containing Paper and Keyword data

    This class assumes that the database has been properly created according to database_setup/create_tables.sql

    Attributes:
        db: MySQLConnection to a database contaning data for this module
    """
    def __init__(self, db: mysql.connector.MySQLConnection):
        self.db = db

    def get_keyword_data(self) -> dict:
        """Get keyword data from FoS table

        Returns: 
            A list of dictionaries in the format
            [
                {
                    "id": int,
                    "keyword": str
                }, ...
            ]
        """
        with self.db.cursor(dictionary=True) as dictcursor:
            dictcursor.execute("""
                SELECT id, keyword
                FROM FoS
            """)
            return dictcursor.fetchall()

    def get_paper_data(self) -> dict:
        """Get paper data from FoS table

        Returns: 
            A list of dictionaries in the format
            [
                {
                    "id": str,
                    "title": str,
                    "abstract": str
                    "citations": int
                }, ...
            ]
        """
        with self.db.cursor(dictionary=True) as dictcursor:
            dictcursor.execute("""
                SELECT id, title, abstract, citations
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

    def store_publication_fos(self, store_data) -> None:
        """
        Stores rows of data into table Publication_FoS

        Args: a list of tuples representing rows of the table, using the following schema:
            [(paper_id, keyword_id, match_score)]
        """
        sql = "REPLACE INTO Publication_FoS (publication_id, FoS_id, score) VALUES (%s, %s, %s)"

        with self.db.cursor() as cursor:
            cursor.executemany(sql, store_data)

        self.db.commit()