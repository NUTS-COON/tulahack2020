FROM python:latest
RUN apt-get update -y
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get -y install tesseract-ocr
RUN apt-get install tesseract-ocr-all
COPY . /app
WORKDIR /app
RUN pip install pillow
RUN pip install pytesseract
RUN pip install opencv-contrib-python
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]