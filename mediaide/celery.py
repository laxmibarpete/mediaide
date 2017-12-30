from __future__ import absolute_import


import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediaide.settings')

app = Celery('mediaide')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()