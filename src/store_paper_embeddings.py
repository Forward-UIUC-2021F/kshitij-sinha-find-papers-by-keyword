# Code skeleton pulled from guidlines/keyword_assignment/store_paper_embeddings.py

import sys
import mysql.connector
from sentence_transformers import SentenceTransformer

from utils import write_pickle_data, concat_paper_info


db = mysql.connector.connect(
  host="localhost",
  user="sandbox",
  password="sandbox",
  database="assign_paper_kwds"
)
cursor = db.cursor()

print("Connected to database")

data_directory = "../data/"
emb_out_file = data_directory + "SB_paper_embeddings.pickle"
idx_out_file = data_directory + "SB_paper_embedding_mag_ids.pickle"

paper_count = 100

cursor.execute(f"""
    SELECT id, title, abstract
    FROM Publication
    WHERE abstract IS NOT NULL
    LIMIT {paper_count}
""")
paper_ts = cursor.fetchall()


print("Loading and preprocessing data/models")
model = SentenceTransformer('bert-base-nli-mean-tokens')

mag_ids = [t[0] for t in paper_ts]
paper_raw = [concat_paper_info(t[1], t[2]) for t in paper_ts]

print("Getting embeddings for " + str(len(paper_raw)) + " papers")
paper_embeddings = model.encode(paper_raw, show_progress_bar=True)

print("Done. Saving data")
write_pickle_data(paper_embeddings, emb_out_file)
write_pickle_data(mag_ids, idx_out_file)