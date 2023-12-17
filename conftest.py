import pytest
from rest_framework.test import APIClient
from gooanalysis.applists.models import Applications
from rest_framework_simplejwt.tokens import RefreshToken
from gooanalysis.tests.factory import AppFactory



@pytest.fixture
def app1():
    return AppFactory()

@pytest.fixture
def app2():
    return AppFactory()
