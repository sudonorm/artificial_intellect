FROM python:3.10-slim-buster

WORKDIR /app
ENV PYTHONUNBUFFERED 1

ENV DASH_DEBUG_MODE False
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt --no-cache-dir

COPY . /app

EXPOSE 8181
