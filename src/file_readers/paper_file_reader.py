import json

class PaperFileReader:
    def __init__(self, id_key: str, title_key: str, abstract_key: str):
        self.id_field = id_key
        self.title_field = title_key
        self.abstract_field = abstract_key

    def read_file(self, filepath: str):
        with open(filepath) as f:
            paper_json = json.load(f)

        paper_data = [{
            'id': paper[self.id_field],
            'title': paper[self.title_field],
            'abstract': paper[self.abstract_field]
        } for paper in paper_json]

        return paper_data

    