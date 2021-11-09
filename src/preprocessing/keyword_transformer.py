from sentence_transformers import SentenceTransformer

class KeywordTransformer:
    def __init__(self, keyword_data, subset_size=None):
        """
        Construct a paper file

        Args:
            keyword_data: A dictionary of keyword names and frequencies
            subset_size: The number of keywords to create embeddings for. If given, 
                the functions will return data for the first 'subset_size' keywords
                in the keyword input
        """
        self.keyword_data = keyword_data
        self.subset_size = subset_size

    def generateEmbeddings(self):
        """
        Generate a 2D Matrix of keyword embeddings. Every row corresponds to a keyword,
        and rows are populated with the keyword's embeddings
        """
        model = SentenceTransformer('bert-base-nli-mean-tokens')

        keyword_data = self.keyword_data if self.subset_size != None else self.keyword_data[:self.subset_size]
        keywords = [d['keyword'] for d in keyword_data]

        return model.encode(keywords, show_progress_bar=True)

    def getEmbeddingsMetadata(self):
        """
        Create a list of dictionaries of keywords, frequency, and embedding index

        Schema:
        [
            {
                "keyword": ... ,
                "id": ... ,
                "frequency": ...
            }
        ]
        """
        metadata = []

        for ind, keyword_entry in enumerate(self.keyword_data):
            if self.subset_size != None and ind > self.subset_size:
                # Only iterate to size of subset
                break
            metadata.append({
                "keyword": keyword_entry['keyword'],
                "id": ind,
                "frequency": keyword_entry["frequency"],
            })

        return metadata
