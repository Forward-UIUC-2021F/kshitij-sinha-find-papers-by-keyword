from sentence_transformers import SentenceTransformer

from .utils import concat_paper_info

class EmbeddingsGenerator():
    def __init__(self):
        self.model = SentenceTransformer('bert-base-nli-mean-tokens')

    def generate_paper_embeddings(self, paper_data: dict):
        """
        Stores the paper embeddings and paper meta into pickle files

        Args:
            paper_data: dictionary containing paper title and abstract, using the folloing schema:
                [
                    {
                        "id": "paper_id"
                        "title": "Sparsity-certifying Graph Decompositions",
                        "abstract": "  We describe a new algorithm, the $(k,\\ell)$-pebble game ..."
                    },
                    ...
                ]
            out_file: the file to store the paper embeddings in
        """
        print("Getting embeddings for " + str(len(paper_data)) + " papers")

        paper_raw = [concat_paper_info(t['title'], t['abstract']) for t in paper_data]

        paper_embeddings = self.model.encode(paper_raw, show_progress_bar=True)
        id_to_emb_ind = {paper["id"]: ind for ind, paper in enumerate(paper_data)}

        return paper_embeddings, id_to_emb_ind

    def generate_keyword_embeddings(self, keyword_data: str):
        """
        Stores the keywords embeddings and keyword meta into pickle files

        Args:
            keywords_data: dictionary of keywords, using the following schema:
                [
                    {
                        "id": "keyword_id",
                        "keyword": "machine learning",
                    },
                    {
                        "id": "keyword_id",
                        "keyword": "deep learning",
                    }
                    ...
                ]
            out_dir: the directory to store the keyword embeddings and metadat pickle files in
        """
        print("Getting embeddings for keywords")

        keywords = [d['keyword'] for d in keyword_data]
        keyword_embeddings = self.model.encode(keywords, show_progress_bar=True)
        id_to_emb_ind = {keyword["id"]: ind for ind, keyword in enumerate(keyword_data)}

        return keyword_embeddings, id_to_emb_ind