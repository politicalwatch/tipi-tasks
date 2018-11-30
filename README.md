# TIPI ALERTS

A list of tasks for celery to manage alerts from users

## Setup

This project uses [pipenv](https://pipenv.readthedocs.io/en/latest/), you
should install pipenv to configure and run this project.

```
$ pipenv install
```

You can find a requirements.txt file too, so if you don't want to install
pipenv you can install all dependencies using normal pip:

```
$ pip install -r requirements.txt
```

## Run

```
$ celery -A tipi worker -l info
```

If you're using pipenv environment you should run with the pipenv run command

```
$ pipenv run "celery -A tipi worker -l info"
```

## Docker

There's a docker-compose for development that deploys a mongodb a redis and the
python app with all deps.

To run this you should edit the .env file in: `dockerdev/.env` and set your
path in the `APP_PATH` variable.

To run all services:

```
$ cd dockerdev
$ docker-compose up -d
```

You'll have three containers running:

 * tipi\_alerts
 * tipi\_db
 * tipi\_redis

You should be able to enter in any of this containers with the `docker exec`, like:

``
# to get a shell
$ docker exec -ti tipi_alerts sh
# to get a python shell
$ docker exec -ti tipi_alerts pipenv run ipython
# to run the test script
$ docker exec -ti tipi_alerts pipenv run ./test-task.py
``

``
$ docker exec -ti tipi_redis sh
``

``
$ docker exec -ti tipi_db sh
``

## Launching a task

To launch a task you should import the task from the `alerts` module and then
call with the delay, for example:

```python
from alerts import test
task = test.test_task.apply_async((3, 2))
```

The task will be sent to the celery queue and will be executed by the broker.

## Contributing

This projects uses [celery](http://docs.celeryproject.org) for all tasks, so
it's really easy to extend the list of tasks available to use in other modules.
