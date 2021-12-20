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