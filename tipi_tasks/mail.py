import sparkpost
from jinja2 import Template
from . import config


def sparkpost_email(recipients, subject, template, mail_config, context={}):
    template = Template(template)
    html = template.render(**context)
    sp = sparkpost.SparkPost(mail_config['API'])
    sp.transmissions.send(
        recipients=recipients,
        from_email='{} <{}>'.format(mail_config['NAME'], mail_config['FROM']),
        subject=subject,
        html=html,
        track_opens=True,
        track_clicks=True
    )


def debug_email(recipients, subject, template, mail_config, context={}):
    print("New email:")
    print("from: {}".format(mail_config['FROM']))
    print("to: {}".format(recipients))
    print("subject: {}".format(subject))
    template = Template(template)
    print(template.render(**context))


def send_email(*args, **kwargs):
    if config.DEBUG:
        return debug_email(*args, **kwargs)
    return sparkpost_email(*args, **kwargs)
