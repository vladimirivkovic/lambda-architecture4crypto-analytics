FROM python:3.8-slim

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENV KAFKA_BROKER="localhost:9092"
ENV SUBREDDIT="funny"

CMD ["python", "-u", "./app.py"]