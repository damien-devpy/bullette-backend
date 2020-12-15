from django.test import TestCase

from contributions.models import Comment
from contributions.serializers import GetCommentSerializer


class TestCommentSerializer(TestCase):
    fixtures = ["users.json", "documents.json", "contributions.json"]

    def setUp(self):
        self.comment = Comment.objects.first()

    def test_that_serializer_allow_comment_update(self):
        data = {"content": "A new content."}

        serializer = GetCommentSerializer(
            self.comment, data=data, partial=True
        )
        serializer.is_valid()
        serializer.save()

        self.comment.refresh_from_db()

        assert self.comment.content == data["content"]

    def test_that_serializer_do_not_allow_update_of_author_field(self):
        data = {"author": 42}

        serializer = GetCommentSerializer(
            self.comment, data=data, partial=True
        )
        serializer.is_valid()
        serializer.save()

        self.comment.refresh_from_db()

        assert self.comment.author.id != data["author"]
