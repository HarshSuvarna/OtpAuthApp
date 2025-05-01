FROM python:3.12-slim-bookworm

RUN apt-get update

RUN apt-get install -y ffmpeg 

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--port", "8080", "--host","0.0.0.0"]