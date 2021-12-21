from .database import Database
from .embeddings_generator import EmbeddingsGenerator
from .assign_paper_keywords import PaperKeywordAssigner
from .utils import write_pickle_data, write_json_data

import mysql.connector

def main():
    pass


if __name__ == "__main__":
    main()


class PaperIndexer():
    """Computes paper data used in rank-papers

    PaperIndexer connects to a MySQL database. 

    PaperIndexer reads from the FoS table and assumes that the tables FoS is already
    filled with keyword data. This table will be used to assign papers to keywords.

    PaperIndexer writes to the Publication and Publication_FoS table
    
    Attributes:
        db: MySQLConnection to a database. 
            The tables Publication, FoS, and Publication_FoS should already be created. 
            See database_setup/create_tables.sql for more details
    """
    def __init__(self, db: mysql.connector.MySQLConnection):
        self.db = db

    def index_papers(self, paper_data, golden_keywords, keyword_embeddings,
                     word_to_other_freq, embeddings_outfile, id_to_emb_ind_outfile) -> None:
        """
        Takes paper data and does the necessary preprocessing to prepare the paper data for ranking.
        This is done in a 3-step process. 

        1)  The paper data is stored in a database
        2)  Embeddings are generated for every paper in the dataset. The embedding matrix and a dictionary
            mapping paper id's to embedding matrix row indices are stored in pickle files
        3)  Keywords are assigned to papers. See assign_paper_keywords.py for more information

        Args:
            paper_data: A list of dictionaries containing paper data, using the following schema:
                [
                    {
                        "id": str,
                        "title": str,
                        "abstract": str,
                        "citations": int,
                    },
                    ...
                ]
                This data will be added to the database, will be used to create paper embeddings, and
                will be used in paper-keyword assignment
            golden_keywords: A list of keywords that will be searched and assigned to the papers. This represents
                the set of all possible keywords that this module can take as its search input.
            paper_embeddings: A np.ndarray representing vector embeddings for every papers in paper_data
            keyword_embeddings: A np.ndarray representing vector embeddings for every keyword in keyword_data
            word_to_other_freq: A dictionary describing how often keywords appear in non-CS publications. Every entry maps
                a keyword string to an int representing the frequency in non-CS papers.
            embeddings_outfile: A file path that will be used to store a pickle file containing a paper-embedding np.ndarry
            id_to_emb_ind_outfile: The fil epath that will be used to store a pickle file containing a dictionary mapping
                paper ids to their corresponding row in the embedding
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

        database.store_publication_fos(assignments)
