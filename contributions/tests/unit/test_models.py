import pytest
from django.db.utils import IntegrityError
from django.test import TestCase

from contributions.models import Vote, VoteValue
from documents.models import Document
from users.models import User


class TestVoteModel(TestCase):
    fixtures = ["documents.json", "users.json"]

    def setUp(self):
        self.document = Document.objects.get(title="Pro or Con")
        self.vote_value = VoteValue.objects.get(value="Con")
        self.user = User.objects.get(id=1)
        self.vote = Vote.objects.create(
            author=self.user, document=self.document, value=self.vote_value
        )

    def test_that_user_cannot_vote_twice(self):
        with pytest.raises(IntegrityError) as err:
            Vote.objects.create(
                author=self.user, document=self.document, value=self.vote_value
            )

        assert (
            'duplicate key value violates unique constraint "unique_vote"'
            in str(err)
        )

    def test_that_user_cannot_vote_for_another_value_that_ones_defined(self):
        self.document = Document.objects.get(title="Yes or No")
        Vote.objects.create(
            author=self.user, document=self.document, value=self.vote_value
        )

        assert self.document.votes.all().count() == 0
