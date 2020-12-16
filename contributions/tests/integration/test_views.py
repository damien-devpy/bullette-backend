from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from config.utils import get_client_with_auth
from documents.models import Document


class TestCreateVoteView(TestCase):
    fixtures = ["users.json", "documents.json"]

    def setUp(self):
        self.user = get_user_model().objects.first()
        self.client = get_client_with_auth(self.user)
        self.document = Document.objects.first()
        self.value = self.document.votes_values.first()
        self.url = reverse("create-vote", args=[self.document.id])
        self.data = {"value": self.value.id}

    def test_user_can_vote(self):
        response = self.client.post(self.url, self.data)
        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_201_CREATED
        assert response_data == self.data

    def test_unauthenticated_user_cannot_vote(self):
        self.client.credentials()
        response = self.client.post(self.url, self.data)
        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_401_UNAUTHORIZED
        assert "Informations d'authentification non fournies." in str(
            response_data
        )


class TestCreateCommentView(TestCase):
    fixtures = ["users.json", "documents.json"]

    def setUp(self):
        self.user = get_user_model().objects.first()
        self.client = get_client_with_auth(self.user)
        self.unauth_client = APIClient()
        self.document = Document.objects.first()
        self.url = reverse("create-comment", args=[self.document.id])
        self.data = {"content": "A new comment."}

    def test_user_can_comment(self):
        response = self.client.post(self.url, self.data)
        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_201_CREATED
        assert response_data == self.data

    def test_unauthenticated_user_cannot_comment(self):
        response = self.unauth_client.post(self.url, self.data)
        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_401_UNAUTHORIZED
        assert "Informations d'authentification non fournies." in str(
            response_data
        )
