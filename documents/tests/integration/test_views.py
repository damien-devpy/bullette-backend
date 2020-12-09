from documents.views import CreateDocumentView
from documents.models import Document
from users.models import User
from django.test import TestCase
from django.shortcuts import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from documents.serializers import DocumentSerializer

def get_token_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }

class TestCreateDocumentView(TestCase):
    fixtures = ['documents_and_contributions.json', 'users.json']

    def setUp(self):
        self.user = User.objects.get(username='username')
        self.admin = User.objects.get(username='admin')
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
            'comments': [],
            'votes': [],
        }

    def test_all_documents_are_displayed(self):
        response = self.client.get(self.url_list_doc, format='json')

        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_200_OK
        assert len(response_data) == Document.objects.all().count()

    def test_admin_user_can_create_a_document(self):
        token = get_token_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token['access'])

        response = self.client.post(self.url_create_doc, self.data, format='json')

        response_data, status_code = response.data, response.status_code

        document = Document.objects.get(title=self.data['title'])
        expected_data = DocumentSerializer(document).data

        assert response_data == expected_data
        assert status_code == status.HTTP_201_CREATED

    def test_non_admin_user_cannot_create_document(self):
        token = get_token_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token['access'])

        response = self.client.post(self.url_create_doc, self.data, format='json')

        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_403_FORBIDDEN
        assert "Vous n'êtes pas autorisé à créer un document" in str(response_data)

    def test_unauthentified_user_cannot_create_a_document(self):
        response = self.client.post(self.url_create_doc, self.data, format='json')

        response_data, status_code = response.data, response.status_code

        assert status_code == status.HTTP_401_UNAUTHORIZED
        assert "Informations d'authentification non fournies." in str(response_data)
