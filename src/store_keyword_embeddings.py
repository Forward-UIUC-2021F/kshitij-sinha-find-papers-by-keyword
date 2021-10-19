import csv
from keyword_transformer import KeywordTransformer
import json

from utils import write_pickle_data

data_directory = "../data/"

# Raw data files
keywords_file = data_directory + "Keywords-Springer-83K.csv"

# Output pickle files
emb_out_file = data_directory + "springer_keyword_embs.pickle"
metadata_out_file = data_directory + "springer_keyword_data.pickle"

print("Loading keyword file")

with open(keywords_file, newline='') as f:
    keyword_data_reader = list(csv.DictReader(f))

keyword_transformer = KeywordTransformer(keyword_data_reader, 100)
print("Files loaded")

print("Loading and preprocessing data/models")


print("Getting embeddings for keywords")
keyword_embeddings = keyword_transformer.generateEmbeddings()
keyword_metadata = keyword_transformer.getEmbeddingsMetadata()

print("Done. Saving data")

write_pickle_data(keyword_embeddings, emb_out_file)
write_pickle_data(keyword_metadata, metadata_out_file)