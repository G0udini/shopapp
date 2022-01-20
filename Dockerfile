FROM python:3.9-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0 \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .