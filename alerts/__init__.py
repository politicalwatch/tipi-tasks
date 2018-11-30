from celery import Celery

from .config import BROKER


app = Celery('tasks', broker=BROKER)


from .test import *
from .validate import *
