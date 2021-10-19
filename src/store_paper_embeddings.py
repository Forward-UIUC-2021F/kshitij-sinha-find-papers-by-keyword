import json
from paper_transformer import PaperTransformer

from utils import write_pickle_data


data_directory = "../data/"

# Raw data files
papers_file = data_directory + "filtered_arxiv.json" # Generated using scripts/generate_small_papers_file.py

# Output pickle files
emb_out_file = data_directory + "SB_paper_embeddings.pickle"
paper_metadata_file = data_directory + "SB_filtered_paper_data.pickle"


print("Loading paper file")

with open(papers_file) as f:
    paper_ts = json.load(f)

paper_transformer = PaperTransformer(paper_ts, 100)

print("Files loaded")

print("Loading and preprocessing data/models")
paper_metadata = paper_transformer.getEmbeddingsMetadata()

print("Getting embeddings for " + str(len(paper_ts)) + " papers")
paper_embeddings = paper_transformer.generateEmbeddings()

print("Done. Saving data")
write_pickle_data(paper_embeddings, emb_out_file)
write_pickle_data(paper_metadata, paper_metadata_file)