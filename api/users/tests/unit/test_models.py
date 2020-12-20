from django.contrib.auth import get_user_model
from django.test import TestCase


class TestUserModel(TestCase):
    def test_user_is_set_citizen_to_false_by_default(self):
        data = {
            "username": "username",
            "email": "test@mail.com",
            "password": "p4ssw0rd_",
        }

        user = get_user_model().objects.create_user(**data)

        assert user.is_citizen is False
