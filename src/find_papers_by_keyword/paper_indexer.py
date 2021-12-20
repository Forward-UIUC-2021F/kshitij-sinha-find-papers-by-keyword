from .database import Database
from .embeddings_generator import EmbeddingsGenerator
from .assign_paper_keywords import PaperKeywordAssigner
from .utils import write_pickle_data, write_json_data


def main():
    pass


if __name__ == "__main__":
    main()


class PaperIndexer():
    def __init__(self, db):
        self.db = db

    def index_papers(self, paper_data, golden_keywords, keyword_embeddings,
                     word_to_other_freq, embeddings_outfile, id_to_emb_ind_outfile):
        """
        Takes paper data and does the necessary preprocessing to prepare the paper data for ranking.
        This is done in a 3-step process. 

        1)  The paper data is stored in a database
        2)  Embeddings are generated for every paper in the dataset. The embedding matrix and a dictionary
            mapping paper id's to embedding matrix row indices are stored in pickle files
        3)  Keywords are assigned to papers. See assign_paper_keywords.py for more information
        """
        paper_data = paper_data[:10]
        database = Database(self.db)
        database.store_paper_data(paper_data)

        embeddings_generator = EmbeddingsGenerator()
        paper_embeddings, paper_id_to_emb_ind = embeddings_generator.generate_paper_embeddings(
            paper_data)

        write_pickle_data(paper_embeddings, embeddings_outfile)
        write_json_data(paper_id_to_emb_ind, id_to_emb_ind_outfile)

        keyword_data = database.get_keyword_data()

        assigner = PaperKeywordAssigner()
        assignments = assigner.assign_paper_keywords(paper_data, keyword_data, golden_keywords,
                                                     paper_embeddings, keyword_embeddings, paper_id_to_emb_ind, word_to_other_freq)

        print(assignments)

        database.store_publication_fos(assignments)
