FROM python:3.12-slim-bookworm

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

WORKDIR /app

CMD uvicorn app:app --port=8080 --host=0.0.0.0