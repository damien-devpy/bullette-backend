from rest_framework import serializers

from .models import Comment, Vote


class CreateOrUpdateCommentSerializer(serializers.ModelSerializer):
    """Exposte field for creation of a comment."""

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
