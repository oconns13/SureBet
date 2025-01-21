import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'surebet.settings')

app = Celery('surebet')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

if hasattr(settings, 'CELERY_HOSTNAME'):
    app.conf.update(hostname=settings.CELERY_HOSTNAME)