import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from gooanalysis.applists.models import Applications
from gooanalysis.applists.selectors import get_apps , get_app_based_on_id ,get_application_ids
import json


@pytest.mark.django_db
def test_get_apps_list(app1, app2):
    apps= get_apps()
    assert len(apps) == 2 and app1 in apps and app2 in apps


@pytest.mark.django_db
def test_get_app(app1, app2):
    app= get_app_based_on_id( app_id=app1.app_id)
    assert app.app_id == app1.app_id
    
@pytest.mark.django_db
def test_get_app_ids(app1, app2):
    apps= get_application_ids()
    assert app1.app_id  in apps and app2.app_id in apps and len(apps) == 2
