from django.db import transaction 
from .models import Applications
from django.db.models import QuerySet


def get_apps():
    return Applications.objects.all()

def get_application_ids():
    applications = Applications.objects.all()
    app_ids = [app.app_id for app in applications]
    return app_ids

