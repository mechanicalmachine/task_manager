import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
class TestFooBarViewSet:
    URL = "/task/"

    def test_create_task(self):
        # TODO move to setup or to factory
        self.user = User.objects.create_user(
            username="test", password="top_secret"
        )
        token = Token.objects.get(user__username='test')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        r = client.post(self.URL, {'name': 'test'})
        assert 201 == r.status_code
