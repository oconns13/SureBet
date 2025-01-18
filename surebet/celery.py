import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'surebet.settings')

app = Celery('surebet')
app.config_from_object('django.conf:settings')
app.conf.broker_url = 'sqs://AKIATBRPQBCHTIQNLFV2:twcI0JvTAXnW8213eKjq0pv+S8PzmrU8BJfdC09H@'
app.autodiscover_tasks()