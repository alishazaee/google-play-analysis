from django.db import transaction 
from .models import Applications
from django.db.models import QuerySet


def get_apps():
    return Applications.objects.all()
