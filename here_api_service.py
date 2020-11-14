import requests
import json

BASE_URL = "https://discover.search.hereapi.com/v1/discover"
TOKEN = ""


def find_pharmacies(lat, lon):
    url = BASE_URL + "?in=circle:{0},{1};r=500&q=pharmacies&apiKey={2}".format(lat, lon, TOKEN)
    resp = requests.get(url)
    data = json.loads(resp.content)

    return list(map(lambda x: (x['title'], '{0}, {1}'.format(x['address']['street'], x['address']['city']), x['distance']), data['items']))
