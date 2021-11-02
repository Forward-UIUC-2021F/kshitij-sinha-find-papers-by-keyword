"""Generate Small Paper File

Script use to shrink the file 'filtered_arxiv.json' for testing purposes.
Loads in JSON data and saves the first 'n' elements to a new file name 'filtered_arxiv_small.json'.
Edit the variable new_paper_count to control the size of the output JSON file.
"""

import json

new_paper_count = 1000
paper_file = "../data/filtered_arxiv.json"
save_file = "../data/filtered_arxiv_small.json"

print(f"Loading from {paper_file}")
with open(paper_file) as f:
    paper_json = json.load(f)

print(f"Extracting first {new_paper_count} paper data")
sliced_json = paper_json[:new_paper_count]

print(f"Saving...")
with open(save_file, "w") as f:
    json.dump(sliced_json, f, indent=2)

print(f"Saved {new_paper_count} entries to file {save_file}")