import pickle

import pcre
from celery import shared_task
from redis import Redis

from tipi_alerts import app
from . import config


def __append_tag_to_founds(tags_found, new_tag):
    found = False
    for tag in tags_found:
        if tag['topic'] == new_tag['topic'] \
                and tag['subtopic'] == new_tag['subtopic'] \
                and tag['tag'] == new_tag['tag']:
                    found = True
                    tag['times'] = tag['times'] + new_tag['times']
                    break
    if not found:
        tags_found.append(new_tag)


def load_redis(value):
    """ Function from flask-caching to load object. """
    if value is None:
        return None
    if value.startswith(b"!"):
        try:
            return pickle.loads(value[1:])
        except pickle.PickleError:
            return None
    try:
        return int(value)
    except ValueError:
        # before 0.8 we did not have serialization.  Still support that.
        return value


@shared_task
def extract_labels_from_text(text, tags=None, cache_key='tags-for-labeling'):
    if not tags:  # recovery from cache. Saved from backend
        conn = Redis(host=config.CACHE_REDIS_HOST, db=config.CACHE_REDIS_DB)
        tags = load_redis(conn.get(cache_key)) or []

    tags_found = []
    text = ''.join(text.splitlines())
    for line in text.split('.'):
        for tag in tags:
            result = pcre.findall(tag['compiletag'], line)
            times = len(result)
            if times > 0:
                tag_copy = tag.copy()
                tag_copy.pop('compiletag')
                tag_copy['times'] = times
                __append_tag_to_founds(tags_found, tag_copy)

    return {
        'topics': sorted(list(set([tag['topic'] for tag in tags_found]))),
        'tags': sorted(tags_found, key=lambda t: (t['topic'], t['subtopic'], t['tag'])),
    }


def check_status_task(task_id):
    task = app.AsyncResult(task_id)
    result = None
    st = task.status
    if st == 'SUCCESS':
        result = task.get()
    return {'status': st, 'result': result}
