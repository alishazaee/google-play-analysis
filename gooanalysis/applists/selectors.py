from django.db import transaction 
from .models import Applications
from django.db.models import QuerySet


def get_apps():
    return Applications.objects.all()


def get_app_based_on_id(* , app_id:str):
    return Applications.objects.get(app_id=app_id)

def get_application_ids():
    applications = Applications.objects.all()
    app_ids = [app.app_id for app in applications]
    return app_ids

