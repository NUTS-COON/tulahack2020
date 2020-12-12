import re
import os

import cv2
import numpy as np
import pytesseract
import uvicorn
from fastapi import FastAPI, Form
from pydantic import BaseModel
from pytesseract import Output
from starlette.middleware.cors import CORSMiddleware

MIN_WORD_WIDTH = 3
RUS_LETTERS_REGEX = r'[а-яА-Я]{1,}'


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def thresholding(img):
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def parse_words(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = thresholding(img_gray)
    d = pytesseract.image_to_data(img_gray, output_type=Output.DICT, lang='rus')
    return list(filter(lambda x: len(x) >= MIN_WORD_WIDTH and re.match(RUS_LETTERS_REGEX, x), set(d['text'])))


def get_words_from_image(img_bytes):
    jpg_as_np = np.frombuffer(img_bytes, dtype=np.uint8)
    image = cv2.imdecode(jpg_as_np, 1)
    return parse_words(image)


class Item(BaseModel):
    media: bytes


@app.get('/check')
async def check():
    return 'ok'

@app.post('/parseImage')
async def extendSearch(media=Form(...)):
    return get_words_from_image(media.file.read())

if __name__ == '__main__':
    port = int(os.environ['SERVICE_PORT'])
    uvicorn.run(app, host="0.0.0.0", port=port)
