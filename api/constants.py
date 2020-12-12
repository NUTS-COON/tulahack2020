import os

MY_SQL_HOST = os.environ['MY_SQL_HOST']
MY_SQL_LOGIN = os.environ['MY_SQL_LOGIN']
MY_SQL_PASSWORD = os.environ['MY_SQL_PASSWORD']
MY_SQL_DATABASE = os.environ['MY_SQL_DATABASE']

ELASTIC_RESPONSE_SIZE = int(os.environ['ELASTIC_RESPONSE_SIZE'])
ELASTIC_BASE_URL = os.environ['ELASTIC_BASE_URL']
ELASTIC_COLLECTION_PATH = os.environ['ELASTIC_COLLECTION_PATH']
ELASTIC_DRUG_SEARCH_PATH = ELASTIC_BASE_URL + ELASTIC_COLLECTION_PATH

HERE_API_KEY = os.environ['HERE_API_KEY']

SERVICE_PORT = int(os.environ['SERVICE_PORT'])