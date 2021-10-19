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

        if self.subset_size != None:
            keyword_csv = self.keyword_data[:self.subset_size]

        return model.encode(keyword_csv, show_progress_bar=True)

    def getEmbeddingsMetadata(self):
        """
        Creates an array of dictionaries containing paper titles, abstracts, and index of 
        their entry in the embedding array
        """
        metadata = []

        for ind, keyword in enumerate(self.keyword_data):
            if self.subset_size != None and ind > self.subset_size:
                # Only iterate to size of subset
                break

            entry = {
                'index': ind,
                'keyword': keyword['keyword'],
                'frequency': keyword['frequency'],
            }
            metadata.append(entry)

        return metadata
