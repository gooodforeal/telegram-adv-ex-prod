FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH="$PYTHONPATH:/src"

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .