from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from config.env import env

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.base')

app = Celery('styleguide_example')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY') IN moshkel saze
app.config_from_object("django.conf:settings")


# https://docs.celeryproject.org/en/stable/userguide/configuration.html

app.conf.broker_url = env('CELERY_BROKER_URL', default='redis://localhost:6379/0')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
