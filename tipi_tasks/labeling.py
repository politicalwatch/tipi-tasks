import codecs
import pickle

import pcre
from celery import shared_task

from tipi_tasks import app
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


@shared_task
def extract_labels_from_text(text, tags):
    tags = pickle.loads(codecs.decode(tags.encode(), "base64"))

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
            'status': 'SUCCESS',
            'excerpt': text if len(text) <= config.SCANNED_TEXT_EXCERPT_SIZE else text[:config.SCANNED_TEXT_EXCERPT_SIZE-3]+' [...]',
            'result': {
                'topics': sorted(list(set([tag['topic'] for tag in tags_found]))),
                'tags': sorted(tags_found, key=lambda t: (t['topic'], t['subtopic'], t['tag'])),
            }
        }


def check_status_task(task_id):
    task = app.AsyncResult(task_id)
    excerpt = None
    result = None
    st = task.status
    if st == 'SUCCESS':
        excerpt = task.get()['excerpt']
        result = task.get()['result']
    return {'status': st,  'excerpt': excerpt,'result': result}
