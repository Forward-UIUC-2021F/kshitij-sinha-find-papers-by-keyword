import csv

class KeywordFileReader:
    def __init__(self, id_key: str, keyword_key: str, frequency_key: str):
        self.id_key = id_key
        self.keyword_key = keyword_key
        self.frequency_key = frequency_key

    def read_file(self, filepath: str):
        with open(filepath, newline='') as f:
            # Use | as quotechar, because Keyword-Springer-83K.csv uses "|" to group entries with commas together
            keyword_data = list(csv.DictReader(f, quotechar="|"))

        # Use row of data in CSV as ID because no given ID field in file
        filtered_data = []
        for ind, entry in enumerate(keyword_data):
            filtered_data.append({
                "id": ind,
                "keyword": entry[self.keyword_key],
                "frequency": entry[self.frequency_key]
            })

        return filtered_data