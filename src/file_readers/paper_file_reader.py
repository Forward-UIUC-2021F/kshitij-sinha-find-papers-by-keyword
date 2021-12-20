import json


class PaperFileReader:
    def __init__(self, id_key: str, title_key: str, abstract_key: str, citations_key: str):
        self.id_field = id_key
        self.title_field = title_key
        self.abstract_field = abstract_key
        self.citations_field = citations_key

        self.text_default = ''
        self.citations_default = 0

    def read_file(self, filepath: str):
        with open(filepath) as f:
            paper_json = json.load(f)

        paper_data = []
        for paper in paper_json:
            entry = {
                'id': paper[self.id_field]
            }

            if self.title_field != None and self.title_field in paper:
                entry['title'] = paper[self.title_field]
            else:
                entry['title'] = self.text_default

            if self.abstract_field != None and self.abstract_field in paper:
                entry['abstract'] = paper[self.abstract_field]
            else:
                entry['abstract'] = self.text_default

            if self.citations_field != None and self.citations_field in paper:
                entry['citations'] = paper[self.citations_field]
            else:
                entry['citations'] = self.citations_default

            paper_data.append(entry)

        return paper_data
