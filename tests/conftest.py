import pytest
from django.conf import settings
from django.test import Client

@pytest.fixture
def client():
    return Client()