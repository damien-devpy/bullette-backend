from django.test import TestCase
from django.contrib.auth import get_user_model

class TestUserModel(TestCase):

    def setUp(self):
        self.data = {"username": "username",
                     "email": "test@mail.com",
                     "password": "p4ssw0rd_",
                     }
        user = get_user_model().objects.create_user(**self.data)

    def test_user_is_set_citizen_to_false_by_default(self):
        user = get_user_model().objects.get(email=self.data['email'])

        assert user.is_citizen is False

