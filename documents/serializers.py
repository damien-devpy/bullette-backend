from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ['id', 'title', 'author', 'content', 'created_at', 'comments', 'votes']