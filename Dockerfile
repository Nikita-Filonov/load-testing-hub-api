FROM python:3.11
ENV PYTHONUNBUFFERED=1

USER root

WORKDIR /app

COPY requirements.txt /app/
RUN apt-get update && apt-get -y install sudo
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 13100