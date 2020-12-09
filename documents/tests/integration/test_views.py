from documents.views import CreateDocumentView
from django.test import TestCase
from django.shortcuts import reverse
from rest_framework.test import APIClient


class TestCreateDocumentView(TestCase):
    permis
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create-document')
        self.data = {
            'author': 'author',
            'type': '',
            'title': 'Lorem ipsum',
            'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            'end_at': None,
            'add_vote': True,
            'locked': False,
            'comments': [],
            'votes': [],
        }

    def test_that_document_is_successfully_create(self):
