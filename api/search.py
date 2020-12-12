import requests
import json
import constants

DRUG_NAMES = set()

with open('names.txt', 'r', encoding='utf8') as f:
    words = f.read().split('\n')
    for w in words:
        DRUG_NAMES.add(w)


def get_query_from_words(words):
    words = map(lambda x: x.lower(), words)
    good_words = list(filter(lambda x: x in DRUG_NAMES, words))[:2]
    return ' '.join(good_words)


def find_drugs(query, size=constants.ELASTIC_RESPONSE_SIZE):
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
    resp = requests.post(constants.ELASTIC_DRUG_SEARCH_PATH + '?size=' + str(size), json=json.loads(query_data))
    data = json.loads(resp.content)
    drugs = data['hits']['hits']
    res = []
    for d in drugs:
        res.append(d['_source'])

    return res
