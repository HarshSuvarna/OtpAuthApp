FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD uvicorn app:app --port=8080 --host=0.0.0.0