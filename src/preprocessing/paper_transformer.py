from sentence_transformers import SentenceTransformer
from utils import concat_paper_info

class PaperTransformer:
    def __init__(self, paper_json, subset_size=None):
        """
        Construct a paper file

        Args:
            paper_file: A json file containing paper ids, titles, abstracts
            subset_size: The number of papers to create embeddings for. If given, 
                the functions will return data for the first 'subset_size' papers
                in the 'paper_file'
        """
        self.paper_json = paper_json
        self.subset_size = subset_size

    def generateEmbeddings(self):
        """
        Generate a 2D Matrix of paper embeddings. Every row correspondings to a paper,
        and rows are populated with the paper's embeddings
        """
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        paper_raw = [concat_paper_info(t['title'], t['abstract']) for t in self.paper_json]

        if self.subset_size != None:
            paper_raw = paper_raw[:self.subset_size]

        return model.encode(paper_raw, show_progress_bar=True)

    def getEmbeddingsMetadata(self):
        """
        Creates an array of dictionaries containing paper titles, abstracts, and index of 
        their entry in the embedding array

        Schema:
        [
            {
                "id": ...
                "arxiv_id": ...
                "title": ...
                "abstract" ...
            }
        ]
        """
        metadata = []

        for ind, paper in enumerate(self.paper_json):
            if self.subset_size != None and ind > self.subset_size:
                # Only iterate to size of subset
                break

            entry = {
                'id': ind,
                'arxiv_id': paper['id'],
                'title': paper['title'],
                'abstract': paper['abstract'],
            }
            metadata.append(entry)

        return metadata
