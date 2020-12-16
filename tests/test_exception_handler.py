import pytest
from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APIClient


def mock_post(*args, **kwargs):
    return 1 / 0


@pytest.fixture
def mocking_post_registration_view(monkeypatch):
    monkeypatch.setattr("users.views.RegistrationView.post", mock_post)


def test_that_exception_handler_properly_manage_500_error(
    mocking_post_registration_view,
):
    data = {
        "email": "test@mail.com",
        "username": "username",
        "password": "password_",
        "password2": "password_",
    }
    client = APIClient()
    url = reverse("signup")
    response = client.post(url, data)

    response_data, status_code = response.data, response.status_code

    assert response_data["error"] == "division by zero"
    assert status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
