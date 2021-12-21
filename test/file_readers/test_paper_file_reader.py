import unittest

from src.file_readers.paper_file_reader import PaperFileReader

class TestPaperFileReader(unittest.TestCase):
    def testNoCitationPaperData(self):
        paper_file = "test_data/papers.json"
        file_reader = PaperFileReader('id', 'title', 'abstract', None)
        papers = file_reader.read_file(paper_file)

        self.assertEqual(len(papers), 10)

        # Check first and last elements
        first = papers[0]
        self.assertEqual(first['id'], "0704.0002")
        self.assertEqual(first['title'], "Sparsity-certifying Graph Decompositions")
        self.assertEqual(first['abstract'], "  We describe a new algorithm, the $(k,\\ell)$-pebble game with colors, and use\nit obtain a characterization of the family of $(k,\\ell)$-sparse graphs and\nalgorithmic solutions to a family of problems concerning tree decompositions of\ngraphs. Special instances of sparse graphs appear in rigidity theory and have\nreceived increased attention in recent years. In particular, our colored\npebbles generalize and strengthen the previous results of Lee and Streinu and\ngive a new proof of the Tutte-Nash-Williams characterization of arboricity. We\nalso present a new decomposition that certifies sparsity based on the\n$(k,\\ell)$-pebble game with colors. Our work also exposes connections between\npebble game algorithms and previous sparse graph algorithms by Gabow, Gabow and\nWestermann and Hendrickson.\n")

        last = papers[-1]
        self.assertEqual(last['id'], "0704.0217")
        self.assertEqual(last['title'], "Capacity of a Multiple-Antenna Fading Channel with a Quantized Precoding\n  Matrix")
        self.assertEqual(last['abstract'], "  Given a multiple-input multiple-output (MIMO) channel, feedback from the\nreceiver can be used to specify a transmit precoding matrix, which selectively\nactivates the strongest channel modes. Here we analyze the performance of\nRandom Vector Quantization (RVQ), in which the precoding matrix is selected\nfrom a random codebook containing independent, isotropically distributed\nentries. We assume that channel elements are i.i.d. and known to the receiver,\nwhich relays the optimal (rate-maximizing) precoder codebook index to the\ntransmitter using B bits. We first derive the large system capacity of\nbeamforming (rank-one precoding matrix) as a function of B, where large system\nrefers to the limit as B and the number of transmit and receive antennas all go\nto infinity with fixed ratios. With beamforming RVQ is asymptotically optimal,\ni.e., no other quantization scheme can achieve a larger asymptotic rate. The\nperformance of RVQ is also compared with that of a simpler reduced-rank scalar\nquantization scheme in which the beamformer is constrained to lie in a random\nsubspace. We subsequently consider a precoding matrix with arbitrary rank, and\napproximate the asymptotic RVQ performance with optimal and linear receivers\n(matched filter and Minimum Mean Squared Error (MMSE)). Numerical examples show\nthat these approximations accurately predict the performance of finite-size\nsystems of interest. Given a target spectral efficiency, numerical examples\nshow that the amount of feedback required by the linear MMSE receiver is only\nslightly more than that required by the optimal receiver, whereas the matched\nfilter can require significantly more feedback.\n")