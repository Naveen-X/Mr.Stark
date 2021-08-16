FROM debian:latest
FROM python:3.9.6-slim-buster
RUN apt update && apt upgrade -y git
RUN apt update && apt upgrade -y ffpmeg
COPY . /app
WORKDIR /app
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt
CMD python3 -m Stark
