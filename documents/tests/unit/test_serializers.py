from unittest.mock import patch

from django.test import TestCase

from documents.models import Document
from documents.serializers import (CreateOrUpdateDocumentSerializer,
                                   GetDocumentSerializer)


class TestGetDocumentSerializer(TestCase):
    fixtures = ["users.json", "documents.json"]

    def setUp(self):
        self.document = Document.documents.get_document_by_id(pk=1)

    def test_that_get_votes_details_method_return_expected_data(self):
        serializer = GetDocumentSerializer(self.document)

        with patch(
            "documents.models.Document.get_votes_values",
            return_value=self.document.votes_values.all(),
        ):
            with patch(
                "documents.models.Document.get_votes_details",
                side_effect=[0, 0],
            ):
                assert serializer.data["votes_details"] == {"Pro": 0, "Con": 0}

    def test_that_get_comments_counts_method_return_expected_data(self):
        serializer = GetDocumentSerializer(self.document)

        with patch(
            "documents.models.Document.get_comments_count", return_value=0
        ):
            assert serializer.data["comments_count"] == 0


class TestCreateOrUpdateDocumentSerializer(TestCase):
    fixtures = ["users.json", "documents.json"]

    def setUp(self):
        self.document = Document.objects.first()

    def test_that_serializer_allow_update_document_instance(self):
        data = {"title": "All new title."}
        serializer = CreateOrUpdateDocumentSerializer(
            self.document, data, partial=True
        )
        serializer.is_valid()
        serializer.save()

        assert self.document.title == data["title"]
