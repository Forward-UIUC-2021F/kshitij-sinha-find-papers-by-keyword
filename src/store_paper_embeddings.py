import json
from sentence_transformers import SentenceTransformer

from utils import write_pickle_data, concat_paper_info


data_directory = "../data/"

# Raw data files
papers_file = data_directory + "filtered_arxiv_small.json" # Generated using scripts/generate_small_papers_file.py
keywords_file = data_directory + "Keywords-Springer-83K.csv"

# Output pickle files
emb_out_file = data_directory + "SB_paper_embeddings.pickle"
idx_out_file = data_directory + "SB_paper_embedding_mag_ids.pickle"

paper_count = 50

print("Loading paper file")

with open(papers_file) as f:
    paper_data = json.load(f)

paper_ts = paper_data[:paper_count]

print("Files loaded")

print("Loading and preprocessing data/models")
model = SentenceTransformer('bert-base-nli-mean-tokens')

mag_ids = [t['id'] for t in paper_ts]
paper_raw = [concat_paper_info(t['title'], t['abstract']) for t in paper_ts]

print("Getting embeddings for " + str(len(paper_raw)) + " papers")
paper_embeddings = model.encode(paper_raw, show_progress_bar=True)

print("Done. Saving data")
write_pickle_data(paper_embeddings, emb_out_file)
write_pickle_data(mag_ids, idx_out_file)