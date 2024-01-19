import sparkpost
from jinja2 import Environment, select_autoescape, Template
from . import config

status_mapping = {
    "Aprobada": "completed",
    "Respondida": "completed",
    "Celebrada": "completed",
    "Convalidada": "completed",
    "Convertida en otra": "completed",
    "Acumulada en otra": "completed",
    "En tramitación": "neutral",
    "Desconocida": "neutral",
    "No admitida a trámite": "error",
    "No debatida": "error",
    "Caducada": "error",
    "Rechazada": "error",
    "Derogada": "error",
    "Retirada": "error",
    "No celebrada": "error"
}

legislative_type_ids = ["120", "121", "122", "123", "124", "125", "127", "130", "131", "132"]
political_orientiation_type_ids = ["161", "162", "171", "173","200", "201", "225", "430"]

def is_in(value, array):
    return value in array

def is_not_in(value, array):
    return value not in array

env = Environment(autoescape=select_autoescape(['html', 'xml']))
env.tests['in'] = is_in
env.tests['not_in'] = is_not_in

def sparkpost_email(recipients, subject, template, mail_config, context={}):
    template = env.from_string(template)
    try:
        html = template.render(**context, status_mapping=status_mapping, legislative_type_ids=legislative_type_ids, political_orientiation_type_ids=political_orientiation_type_ids)
    except Exception as e:
        print(f"Template error: {e}")
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
