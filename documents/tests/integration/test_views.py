from documents.models import Document
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APIClient
from documents.serializers import GetDetailDocumentSerializer, CreateOrUpdateDocumentSerializer
from config.commons import get_client_with_auth
import pytest
import pdb

class TestCreateDocumentView(TestCase):
    fixtures = ['documents.json', 'users.json']

    def setUp(self):
        self.user = get_user_model().objects.get(username='username')
        self.admin = get_user_model().objects.get(username='admin')
        self.url_create_doc = reverse('create-document')
        self.url_list_doc = reverse('list-document')
        self.unauth_client = APIClient()
        self.data = {
            'type': 1,
            'title': 'Lorem ipsum',
            'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            'end_at': None,
            'add_vote': True,
            'is_locked': False,
            'votes_values': ['Yes', 'No']
        }

    def test_all_documents_are_displayed(self):
        response = self.unauth_client.get(self.url_list_doc)

        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_200_OK
        assert len(response_data) == Document.objects.all().count()

    def test_admin_user_can_create_a_document(self):
        client = get_client_with_auth(self.admin)

        response = client.post(self.url_create_doc, self.data)

        response_data, status_code = response.data, response.status_code

        document = Document.objects.get(title=self.data['title'])
        expected_data = CreateOrUpdateDocumentSerializer(document).data

        assert status_code == status.HTTP_201_CREATED
        assert response_data == expected_data

    def test_non_admin_user_cannot_create_document(self):
        client = get_client_with_auth(self.user)

        response = client.post(self.url_create_doc, self.data)

        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_403_FORBIDDEN
        assert "Vous n'êtes pas autorisé à effectuer cette action" in str(response_data)

    def test_unauthentified_user_cannot_create_a_document(self):
        response = self.unauth_client.post(self.url_create_doc, self.data)

        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_401_UNAUTHORIZED
        assert "Informations d'authentification non fournies." in str(response_data)


class TestGetUpdateDestroyDocumentView(TestCase):
    fixtures = ['users.json', 'documents.json', 'contributions.json']

    def setUp(self):
        self.document = Document.objects.first()
        self.url = reverse('get-update-delete-document', args=[self.document.id])
        self.admin = get_user_model().objects.get(username='admin')
        self.client = get_client_with_auth(self.admin)

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
        assert response_data == GetDetailDocumentSerializer(self.document).data

