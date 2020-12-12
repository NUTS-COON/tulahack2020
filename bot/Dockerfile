FROM python:latest
COPY . /bot
WORKDIR /bot
RUN apt-get update -y
RUN pip install opencv-python
RUN pip install pytesseract
RUN pip install numpy
RUN pip install requests
RUN pip install pyTelegramBotAPI
ENTRYPOINT ["python"]
CMD ["bot.py"]
