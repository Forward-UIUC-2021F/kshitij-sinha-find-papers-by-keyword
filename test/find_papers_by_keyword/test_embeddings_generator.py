import unittest

import numpy as np
from sentence_transformers import SentenceTransformer
from src.find_papers_by_keyword.embeddings_generator import EmbeddingsGenerator
from src.file_readers.paper_file_reader import PaperFileReader

class TestPaperEmbeddings(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.embeddings_generator = EmbeddingsGenerator()

        paper_file = "test_data/papers.json"
        file_reader = PaperFileReader('id', 'title', 'abstract', None)
        papers = file_reader.read_file(paper_file)
        cls.embeddings, cls.id_to_ind = cls.embeddings_generator.generate_paper_embeddings(papers)

    def testEmbeddingsShape(self):
        self.assertEqual(self.embeddings.shape, (10, 768))

    def testEmbeddingValues(self):
        first_paper_raw = "Sparsity-certifying Graph Decompositions. We describe a new algorithm, the $(k,\\ell)$-pebble game with colors, and use\nit obtain a characterization of the family of $(k,\\ell)$-sparse graphs and\nalgorithmic solutions to a family of problems concerning tree decompositions of\ngraphs. Special instances of sparse graphs appear in rigidity theory and have\nreceived increased attention in recent years. In particular, our colored\npebbles generalize and strengthen the previous results of Lee and Streinu and\ngive a new proof of the Tutte-Nash-Williams characterization of arboricity. We\nalso present a new decomposition that certifies sparsity based on the\n$(k,\\ell)$-pebble game with colors. Our work also exposes connections between\npebble game algorithms and previous sparse graph algorithms by Gabow, Gabow and\nWestermann and Hendrickson.\n"
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        first_embedding = model.encode(first_paper_raw)

        np.testing.assert_almost_equal(self.embeddings[0], first_embedding)