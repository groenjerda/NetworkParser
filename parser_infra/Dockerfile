FROM python:3.12-slim

WORKDIR /NetworkParser
COPY ./ ./
RUN apt update && apt -y upgrade
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt --no-cache-dir
