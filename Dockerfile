# FROM ubuntu:20.04

FROM python:3.8
MAINTAINER KDH
#ENV PYTHONUNBUFFERD 1

RUN apt-get update

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./cmd_light /app
CMD python main.py ${URL} ${PORT} ${TOPIC} ${DEVICE}