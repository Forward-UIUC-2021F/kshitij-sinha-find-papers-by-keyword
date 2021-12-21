import unittest

from src.find_papers_by_keyword.assign_paper_keywords import PaperKeywordAssigner
from src.find_papers_by_keyword.embeddings_generator import EmbeddingsGenerator

def split_assignment_tuples(assignments):
    assignment_pairs = [a[:2] for a in assignments]
    scores = [a[-1] for a in assignments]
    return assignment_pairs, scores


class TestPaperKeywordAssignerClassifications(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.assigner = PaperKeywordAssigner()
        cls.embedding_generator = EmbeddingsGenerator()

        cls.paper_data = [
            {
                "id": "1",
                "title": "machine learning",
                "abstract": "mock paper about machine learning"
            },
            {
                "id": "2",
                "title": "systems",
                "abstract": "mock paper about systems"
            }
        ]

        cls.paper_embs, cls.paper_id_to_ind = cls.embedding_generator.generate_paper_embeddings(
            cls.paper_data)

    def testUnassignedKeyword(self):
        keyword_data = [
            {"id": 0, "keyword": "machine learning"},
            {"id": 1, "keyword": "systems"},
            {"id": 2, "keyword": "security"}
        ]
        golden_keywords = ["machine learning", "systems", "security"]

        # no frequency penalization
        word_to_other_freq = {keyword: 1 for keyword in golden_keywords}
        keyword_embs = self.embedding_generator.generate_keyword_embeddings(
            keyword_data)[0]

        assignments = self.assigner.assign_paper_keywords(self.paper_data, keyword_data, golden_keywords,
                                                          self.paper_embs, keyword_embs, self.paper_id_to_ind,
                                                          word_to_other_freq)

        assignment_pairs, scores = split_assignment_tuples(assignments)
        expected_pairs = [("1", 0), ("2", 1)]

        self.assertEqual(assignment_pairs, expected_pairs)
        for score in scores:
            self.assertTrue(0 <= score <= 1)         

    def testUnassignedPaper(self):
        keyword_data = [
            {"id": 0, "keyword": "machine learning"},
        ]
        golden_keywords = ["machine learning"]

        # no frequency penalization
        word_to_other_freq = {keyword: 1 for keyword in golden_keywords}
        keyword_embs = self.embedding_generator.generate_keyword_embeddings(
            keyword_data)[0]

        assignments = self.assigner.assign_paper_keywords(self.paper_data, keyword_data, golden_keywords,
                                                          self.paper_embs, keyword_embs, self.paper_id_to_ind,
                                                          word_to_other_freq)

        assignment_pairs, scores = split_assignment_tuples(assignments)
        expected_pairs = [("1", 0)]

        self.assertEqual(assignment_pairs, expected_pairs)
        for score in scores:
            self.assertTrue(0 <= score <= 1)                    

    def testExtraGoldenKeywords(self):
        keyword_data = [
            {"id": 0, "keyword": "machine learning"},
        ]
        golden_keywords = ["machine learning", "systems"]

        # no frequency penalization
        word_to_other_freq = {keyword: 1 for keyword in golden_keywords}
        keyword_embs = self.embedding_generator.generate_keyword_embeddings(
            keyword_data)[0]

        assignments = self.assigner.assign_paper_keywords(self.paper_data, keyword_data, golden_keywords,
                                                          self.paper_embs, keyword_embs, self.paper_id_to_ind,
                                                          word_to_other_freq)

        assignment_pairs, scores = split_assignment_tuples(assignments)
        expected_pairs = [("1", 0)]

        self.assertEqual(assignment_pairs, expected_pairs)
        for score in scores:
            self.assertTrue(0 <= score <= 1) 

    def testMissingGoldenKeywords(self):
        keyword_data = [
            {"id": 0, "keyword": "machine learning"},
            {"id": 1, "keyword": "systems"},
            {"id": 2, "keyword": "security"}
        ]
        golden_keywords = ["machine learning"]

        # no frequency penalization
        word_to_other_freq = {keyword: 1 for keyword in golden_keywords}
        keyword_embs = self.embedding_generator.generate_keyword_embeddings(
            keyword_data)[0]

        assignments = self.assigner.assign_paper_keywords(self.paper_data, keyword_data, golden_keywords,
                                                          self.paper_embs, keyword_embs, self.paper_id_to_ind,
                                                          word_to_other_freq)

        assignment_pairs, scores = split_assignment_tuples(assignments)
        expected_pairs = [("1", 0)]

        self.assertEqual(assignment_pairs, expected_pairs)
        for score in scores:
            self.assertTrue(0 <= score <= 1) 

class TestPaperKeywordAssignerScores(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.assigner = PaperKeywordAssigner()
        cls.embedding_generator = EmbeddingsGenerator()

        cls.paper_data = [
            {
                "id": "0",
                "title": "paper 0",
                "abstract": "learning learning security"
            },
            {
                "id": "1",
                "title": "paper 1",
                "abstract": "learning security security"
            }
        ]

        cls.paper_embs, cls.paper_id_to_ind = cls.embedding_generator.generate_paper_embeddings(
            cls.paper_data)

    def testStrongerPaperMatches(self):
        keyword_data = [
            {"id": 0, "keyword": "learning"},
        ]
        golden_keywords = ["learning"]

        # no frequency penalization
        word_to_other_freq = {keyword: 1 for keyword in golden_keywords}
        keyword_embs = self.embedding_generator.generate_keyword_embeddings(
            keyword_data)[0]

        assignments = self.assigner.assign_paper_keywords(self.paper_data, keyword_data, golden_keywords,
                                                          self.paper_embs, keyword_embs, self.paper_id_to_ind,
                                                          word_to_other_freq)
        assignment_pairs, scores = split_assignment_tuples(assignments)
        expected_pairs = [("0", 0), ("1", 0)]

        self.assertEqual(assignment_pairs, expected_pairs)

        # Paper 0 is better match to machine learning than Paper 1
        paper_0_score, paper_1_score = scores
        self.assertGreater(paper_0_score, paper_1_score)  

    def testStrongerKeywordMatches(self):
        keyword_data = [
            {"id": 0, "keyword": "learning"},
            {"id": 1, "keyword": "security"},
        ]
        golden_keywords = ["learning", "security"]

        # no frequency penalization
        word_to_other_freq = {keyword: 1 for keyword in golden_keywords}
        keyword_embs = self.embedding_generator.generate_keyword_embeddings(
            keyword_data)[0]

        assignments = self.assigner.assign_paper_keywords(self.paper_data, keyword_data, golden_keywords,
                                                          self.paper_embs, keyword_embs, self.paper_id_to_ind,
                                                          word_to_other_freq)
        assignment_pairs, scores = split_assignment_tuples(assignments)
        expected_pairs = [("0", 0), ("0", 1), ("1", 1), ("1", 0)]

        self.assertEqual(assignment_pairs, expected_pairs)

        # Paper 0 matches keyword 0 better than keyword 1
        self.assertGreater(scores[0], scores[1])

        # Paper 1 matches keyword 1 better than keyword 0
        self.assertGreater(scores[2], scores[3])

    def testPenalizeWeakWords(self):
        keyword_data = [
            {"id": 0, "keyword": "learning"},
        ]   
        golden_keywords = ["learning"]
        keyword_embs = self.embedding_generator.generate_keyword_embeddings(
            keyword_data)[0]

        frequency_no_penalty = {"learning": 1}
        assignments_no_penalty = self.assigner.assign_paper_keywords(self.paper_data, keyword_data, golden_keywords,
                                                          self.paper_embs, keyword_embs, self.paper_id_to_ind,
                                                          frequency_no_penalty)

        frequency_penalty = {"learning": 2000}
        assignments_penalty = self.assigner.assign_paper_keywords(self.paper_data, keyword_data, golden_keywords,
                                                          self.paper_embs, keyword_embs, self.paper_id_to_ind,
                                                          frequency_penalty)

        for no_penalty_match, penalty_match in zip(assignments_no_penalty, assignments_penalty):
            no_penalty_score = no_penalty_match[2]
            penalty_score = penalty_match[2]

            self.assertGreater(no_penalty_score, penalty_score)
