import requests
import json

SIZE = '5'
ELASTIC_BASE_URL = 'http://localhost:9200'
ELASTIC_DRUG_SEARCH_PATH = ELASTIC_BASE_URL + '/products/product/_search?size=' + SIZE

DRUG_NAMES = set()

with open('names.txt', 'r', encoding='utf8') as f:
    words = f.read().split('\n')
    for w in words:
        DRUG_NAMES.add(w)


def get_query_from_words(words):
    words = map(lambda x: x.lower(), words)
    good_words = list(filter(lambda x: x in DRUG_NAMES, words))[:2]
    return ' '.join(good_words)


def find_drugs(query):
    query_data = json.dumps({
        "query": {
            "match": {
                "name": {
                    "query": query,
                    "fuzziness": "auto"
                }
            }
        }
    }, ensure_ascii=False)
    resp = requests.post(ELASTIC_DRUG_SEARCH_PATH, json=json.loads(query_data))
    data = json.loads(resp.content)
    drugs = data['hits']['hits']
    res = []
    for d in drugs:
        res.append((d['_source']['id'], d['_source']['name'], d['_source']['price'], d['_source']['manufacturer'], d['_source']['expires']))

    return res
