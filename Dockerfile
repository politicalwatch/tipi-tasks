FROM python:3.6-slim

RUN apt-get update && apt-get install -y git gcc libpcre3-dev
RUN pip install --upgrade pip

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

CMD celery -A tipi_tasks worker -B -l info --logfile=/tmp/celery.log
