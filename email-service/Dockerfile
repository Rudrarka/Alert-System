FROM python:3.8-slim

# layer caching for faster builds
COPY requirements.txt /
RUN pip install -r /requirements.txt

ADD . /email-service
WORKDIR /email-service

ENTRYPOINT celery -A task worker --pool=solo --loglevel=info
