import basket
import search as elastic_search
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/search')
async def search(query):
    return elastic_search.find_drugs(query)


@app.get('/searchByWords')
async def search_by_words(words):
    query = elastic_search.get_query_from_words(words.split('|'))
    return elastic_search.find_drugs(query)


@app.post('/addToBasket')
async def add_to_basket(user_id, product_id):
    return basket.add(user_id, product_id)


@app.post('/removeFromBasket')
async def remove_from_basket(user_id, product_id):
    basket.remove(user_id, product_id)


@app.get('/getBasket')
async def get_basket(user_id):
    return basket.get_basket(user_id)


@app.post('/makeOrder')
async def make_order(user_id):
    basket.make_order(user_id)


uvicorn.run(app, host="0.0.0.0", port=3001)
