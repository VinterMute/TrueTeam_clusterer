FROM python:3.8-slim

WORKDIR /opt/app
COPY . /opt/app

RUN pip3 install -r requirements.txt
