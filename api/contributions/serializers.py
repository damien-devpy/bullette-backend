from rest_framework import serializers

from .models import Comment, Vote, VoteValue


class CreateOrUpdateCommentSerializer(serializers.ModelSerializer):
    """Expose field for creation or update of a comment."""

    class Meta:
        model = Comment
        fields = ["content"]

    def update(self, instance, validated_data):

        for field in validated_data:
            setattr(instance, field, validated_data.get(field))
        instance.save()
        return instance


class GetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {"author": {"read_only": True}}


class CreateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["value"]


class GetVotesDetailsSerializer(serializers.ModelSerializer):
    """Expose votes details about this document.

    Attributes:
        id (int): id of the vote value
        value (str): string value
        count (int): How many vote for this value
    """

    count = serializers.SerializerMethodField()

    class Meta:
        model = VoteValue
        fields = ["id", "value", "count"]

    def get_count(self, obj):
        """Count how many votes for the current value exist in the parent object (document)."""
        return self.context["parent_obj"].get_votes_details(obj.id)
