import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
class TestFooBarViewSet:
    URL = "/task"

    def test_create_task(self):
        # TODO move to setup or to factory
        self.user = User.objects.create_user(
            username="test", password="top_secret"
        )
        token = Token.objects.get(user__username='test')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        data = {
            "name": "test",
            "params": {
                "param1": "some param",
                "param2": "some another param",
            },
            "options": {
                "retry": 2,
                "delay": 3000,
            }
        }
        r = client.post(self.URL, data=data, format='json')
        assert r.status_code == 201

    def test_tasks_list(self, task_factory):
        # TODO move to setup or to factory
        self.user = User.objects.create_user(
            username="test", password="top_secret"
        )
        token = Token.objects.get(user__username='test')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        for i in range(5):
            task_factory()
        for i in range(5):
            task_factory(task_name='test')

        params = {"name": "test"}
        r = client.get(self.URL, params)

        assert r.status_code == 200
        assert len(r.json()) == 5
