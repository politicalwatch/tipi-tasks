FROM python:3.12-slim

RUN apt-get update && apt-get install -y git gcc

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

CMD celery -A tipi_tasks worker -B -l info
