from elasticsearch import Elasticsearch
from store_keywords_es import main
from pprint import pprint


def findSimilarKeywords(client: Elasticsearch, index: str, keyword: str):
    body = {
        "query": {
            "match": {
                "keyword": {
                    "query": "machine learning",
                    "fuzziness": 2
                }
            }
        }
    }

    return client.search(index=index, body=body)


def main():
    es = Elasticsearch()
    pprint(findSimilarKeywords(es, "fos", "machine learning"))


if __name__ == "__main__":
    main()
