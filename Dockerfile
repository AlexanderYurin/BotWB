FROM python:3.11-alpine3.16
COPY . /bot
WORKDIR /bot

RUN pip install --no-cache-dir -r requirements.txt
