import pickle
import json


def pickleToJson(in_filepath, out_filepath):
    with open(in_filepath, "rb") as f:
        p = pickle.load(f)
    with open(out_filepath, "w") as f:
        json.dump(p, f, indent=2)

pickleToJson("../data/springer_keyword_data.pickle", "../schemas/keyword_metadata.json")
pickleToJson("../data/SB_filtered_paper_data.pickle", "../schemas/paper_metadata.json")