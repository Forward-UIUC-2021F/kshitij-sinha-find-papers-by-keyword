import unittest

from src.find_papers_by_keyword.paper_search_engine import PaperSearchEngine
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
        self.assertEqual(len(results[0]), 4)    # each entry is tuple of size 2

    def testArxivMatchScore(self):
        # Tests that the query works as intended, NOT  that the match score is computed correctly
        # For this test to pass, the data in the database must be from filtered_arxiv.json
        result = self.search_engine.compute_match_score("0704.0002", 1052)
        print(result)
        self.assertAlmostEqual(result, 0.002487946947888709)