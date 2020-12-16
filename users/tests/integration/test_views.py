import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from config.utils import get_client_with_auth
from users.models import User
from users.serializers import CreateOrUpdateUserSerializer


class TestRegistrationView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("signup")
        self.data = {
            "username": "username",
            "email": "test@mail.com",
            "password": "p4ssw0rd_",
            "password2": "p4ssw0rd_",
            "is_citizen": True,
        }

        self.expected_data = {
            "username": "username",
            "email": "test@mail.com",
            "is_citizen": True,
        }

    def test_user_signup_successfully(self):
        response = self.client.post(self.url, self.data)

        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_200_OK
        assert "access" in response_data

    def test_user_get_registered_after_signing_up(self):
        self.client.post(self.url, self.data)

        user = User.objects.get(email=self.data["email"])
        registered_data = CreateOrUpdateUserSerializer(user).data

        assert self.expected_data.items() <= registered_data.items()

    def test_user_signing_up_with_invalid_data_return_bad_request_error(self):
        self.data["email"] = "not_an_email"

        serializer = CreateOrUpdateUserSerializer(data=self.data)
        serializer.is_valid()
        expected_data = serializer.errors

        response = self.client.post(self.url, self.data)
        response_data, status_code = response.data, response.status_code

        assert response_data == expected_data
        assert status_code == status.HTTP_400_BAD_REQUEST

    def test_user_signing_up_with_invalid_data_return_bad_request_error2(self):
        self.data["password2"] = "a_different_password"

        serializer = CreateOrUpdateUserSerializer(data=self.data)
        serializer.is_valid()
        expected_data = serializer.errors

        response = self.client.post(self.url, self.data)
        response_data, status_code = response.data, response.status_code

        assert response_data == expected_data
        assert status_code == status.HTTP_400_BAD_REQUEST


class TestUpdateUserView(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.url = reverse("update-password")
        self.user = get_user_model().objects.first()
        self.client = get_client_with_auth(self.user)

    def test_that_user_can_update_his_password(self):
        data = {"password": "a_new_password", "password2": "a_new_password"}
        response = self.client.patch(self.url, data=data)

        status_code = response.status_code
        self.user = get_user_model().objects.first()

        assert check_password(data["password"], self.user.password)
        assert status_code == status.HTTP_204_NO_CONTENT

    def test_that_user_can_update_other_informations(self):
        data = {"username": "a_new_username"}
        response = self.client.patch(self.url, data=data)

        status_code = response.status_code
        self.user.refresh_from_db()
        assert self.user.username == data["username"]
        assert status_code == status.HTTP_204_NO_CONTENT


class TestDeleteUserView(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.url = reverse("delete-user")
        self.user = get_user_model().objects.get(id=1)
        self.client = get_client_with_auth(self.user)

    def test_that_user_can_delete_its_own_account(self):
        response = self.client.delete(self.url)

        status_code = response.status_code

        with pytest.raises(get_user_model().DoesNotExist) as err:
            get_user_model().objects.get(id=1)

        assert "User matching query does not exist" in str(err)
        assert status_code == status.HTTP_200_OK
