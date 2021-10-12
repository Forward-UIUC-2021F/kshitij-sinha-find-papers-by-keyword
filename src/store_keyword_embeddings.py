import csv
from sentence_transformers import SentenceTransformer

from utils import write_pickle_data, concat_paper_info


data_directory = "../data/"

# Raw data files
keywords_file = data_directory + "Keywords-Springer-83K_small.csv"

# Output pickle files
emb_out_file = data_directory + "springer_keyword_embs.pickle"

paper_count = 50

print("Loading paper file")

with open(keywords_file, newline='') as f:
    keyword_data_reader = list(csv.DictReader(f))

print(len(keyword_data_reader))
print("Files loaded")

print("Loading and preprocessing data/models")
model = SentenceTransformer('bert-base-nli-mean-tokens')

print("Getting embeddings for keywords")
keyword_embeddings = model.encode(keyword_data_reader, show_progress_bar=True)

print("Done. Saving data")

write_pickle_data(keyword_embeddings, emb_out_file)