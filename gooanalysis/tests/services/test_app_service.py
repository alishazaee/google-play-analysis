import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from gooanalysis.applists.models import Applications
from gooanalysis.applists.selectors import get_apps , get_app_based_on_id ,get_application_ids
from gooanalysis.applists.services import create_app
import json

@pytest.mark.django_db
def test_create_app():
    a = create_app(app_id="com.example", name="name" , category="social")

    assert a.app_id == "com.example"
    assert a.name == "name"
    assert a.category == "social"