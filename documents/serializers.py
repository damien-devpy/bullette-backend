from rest_framework import serializers
from .models import Document
from contributions.serializers import CommentSerializer


class CreateOrUpdateDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ['id', 'author', 'type', 'title', 'content', 'end_at', 'add_vote', 'is_locked',]
        extra_kwargs = {'id': {'read_only': True},
                        'end_at': {'allow_null': True},
                        }

    def update(self, instance, validated_data):
        for field in validated_data:
            setattr(instance, field, validated_data.get(field))
        instance.save()
        return instance


class GetDocumentSerializer(serializers.ModelSerializer):
    """Expose fields of a document.

    This serializer is intent to be used to list severals documents.
    For exposing more details about documents, GetDetailDocumentSerializer should be used.
    """
    votes_details = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'author', 'type', 'title', 'content', 'created_at', 'end_at', 'comments_count', 'is_locked', 'votes_details']

    def get_votes_details(self, obj):
        votes_details = {}
        for value in obj.get_votes_values():
            votes_details.update({value.value: obj.get_votes_details(value.id)})
        return votes_details

    def get_comments_count(self, obj):
        return obj.get_comments_count()



class GetDetailDocumentSerializer(GetDocumentSerializer):
    """Expose a document with full details about it.

    Such as edit date or a full list of comments.
    """

    comments_details = CommentSerializer(source='get_comments', many=True)

    class Meta:
        model = Document
        fields = ['id', 'author', 'type', 'title', 'content', 'created_at', 'edit_at', 'end_at', 'add_vote', 'is_locked', 'comments_details', 'votes_details']

