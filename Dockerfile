from python:alpine

RUN apk add --no-cache git gcc libc-dev
RUN pip install --upgrade pip
RUN pip install pipenv

ENV PIPENV_VENV_IN_PROJECT=1
WORKDIR /app
COPY . /app/
RUN pipenv install

CMD pipenv run celery -A tipi_alerts worker -B -l info
