import json

filepath = "data/mag_papers_3.txt"
outpath = "data/mag_papers_.json"

with open(filepath, 'r') as f:
    json_list = []
    for json_obj in f:
        json_list.append(json.loads(json_obj))

with open(outpath, 'w') as f:
    json.dump(json_list, f)