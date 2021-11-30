import csv
from elasticsearch import Elasticsearch, helpers

# Generator pattern for efficient bulk indexing
def generate_keyword_data(index, keywords_file):
    keys_to_extract = ['keyword', 'frequency']
    with open(keywords_file, newline='') as f:
        keyword_data = csv.DictReader(f, quotechar="|")

        for i, keyword_entry in enumerate(keyword_data):
            entry_to_store = {key: keyword_entry[key]
                              for key in keys_to_extract}

            if i % 10000 == 0:
                print(f"On {i}th keyword")

            yield {
                "_index": index,
                "_source": entry_to_store
            }

def main():
    es = Elasticsearch()
    index = "fos"
    keywords_file = "../data/Keywords-Springer-83K.csv"

    # Add data
    print("Indexing keywords")
    helpers.bulk(es, generate_keyword_data(index, keywords_file))


if __name__ == "__main__":
    main()
