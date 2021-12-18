import unittest

import src
from src import paper_search_engine
import mysql.connector

class TestRankPapers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db = mysql.connector.connect(
            host="localhost",
            user="forward",
            password="forward",
            database="assign_paper_kwds"
        )
        cls.cur = db.cursor()

    @classmethod
    def teatDownClass(cls):
        cls.cur.close()


    def setUp(self):
        print("nothing")