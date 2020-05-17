FROM python:3.6-alpine3.8

RUN apk add --no-cache build-base bash


RUN mkdir /src
RUN python3 -m venv /src/venv

RUN source /src/venv/bin/activate && pip install -r /src/requirements.txt

COPY stream.py /src/stream.py
COPY requirements.txt /src/requirements.txt
