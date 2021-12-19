import unittest

from src.rank_papers import PaperSearchEngine
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
        cls.search_engine = PaperSearchEngine(db)

    def testOutputShape(self):
        results = self.search_engine.get_relevant_papers_by_id((1,), 1)
        self.assertEqual(len(results), 1)       # search_limit = 1
        self.assertEqual(len(results[0]), 2)    # each entry is tuple of size 2