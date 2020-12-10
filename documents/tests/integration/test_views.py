from documents.models import Document
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.shortcuts import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from documents.serializers import DocumentSerializer
import pytest
import pdb

def get_token_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }


class TestCreateDocumentView(TestCase):
    fixtures = ['documents.json', 'users.json']

    def setUp(self):
        self.user = get_user_model().objects.get(username='username')
        self.admin = get_user_model().objects.get(username='admin')
        self.client = APIClient()
        self.url_create_doc = reverse('create-document')
        self.url_list_doc = reverse('list-document')
        self.data = {
            'type': 1,
            'title': 'Lorem ipsum',
            'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            'end_at': None,
            'add_vote': True,
            'locked': False,
            'votes_values': ['Yes', 'No']
        }

    def test_all_documents_are_displayed(self):
        response = self.client.get(self.url_list_doc)

        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_200_OK
        assert len(response_data) == Document.objects.all().count()

    def test_admin_user_can_create_a_document(self):
        token = get_token_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token['access'])

        response = self.client.post(self.url_create_doc, self.data)

        response_data, status_code = response.data, response.status_code

        document = Document.objects.get(title=self.data['title'])
        expected_data = DocumentSerializer(document).data

        assert status_code == status.HTTP_201_CREATED
        assert response_data == expected_data

    def test_non_admin_user_cannot_create_document(self):
        token = get_token_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token['access'])

        response = self.client.post(self.url_create_doc, self.data)

        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_403_FORBIDDEN
        assert "Vous n'êtes pas autorisé à effectuer cette action" in str(response_data)

    def test_unauthentified_user_cannot_create_a_document(self):
        response = self.client.post(self.url_create_doc, self.data)

        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_401_UNAUTHORIZED
        assert "Informations d'authentification non fournies." in str(response_data)


class TestGetUpdateDestroyDocumentView(TestCase):
    fixtures = ['users.json', 'documents.json', 'contributions.json']

    def setUp(self):
        self.document = Document.objects.first()
        self.client = APIClient()
        self.admin = get_user_model().objects.get(username='admin')
        token = get_token_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token['access'])
        self.url = reverse('get-update-delete-document', args=[self.document.id])

    def test_admin_can_delete_document(self):
        response = self.client.delete(self.url)

        with pytest.raises(Document.DoesNotExist) as err:
            self.document.refresh_from_db()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert 'Document matching query does not exist' in str(err)

    def test_admin_can_update_document(self):
        data = {
            'title': 'Title as been changed.'
        }

        response = self.client.patch(self.url, data)
        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_200_OK
        assert response_data['title'] == data['title']

    def test_that_unauthentified_can_get_document(self):
        self.client.credentials()
        response = self.client.get(self.url)

        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_200_OK
        assert response_data == DocumentSerializer(self.document).data

