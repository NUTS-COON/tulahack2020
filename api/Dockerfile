FROM tiangolo/uvicorn-gunicorn:python3.8
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["store_api.py"]