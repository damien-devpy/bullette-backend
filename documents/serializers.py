from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ['id', 'author', 'type', 'title', 'content', 'created_at', 'edit_at', 'end_at', 'add_vote', 'locked', 'comments', 'votes']
        extra_kwargs = {'created_at': {'read_only': True},
                        'edit_at': {'read_only': True},
                        'comments': {'read_only': True},
                        'votes': {'read_only': True},
                        }