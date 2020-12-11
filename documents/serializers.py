from rest_framework import serializers
from .models import Document
from contributions.models import VoteValue

class DocumentSerializer(serializers.ModelSerializer):

    votes_values = serializers.SlugRelatedField(many=True, queryset=VoteValue.objects.all(), slug_field='value')
    votes_details = serializers.SerializerMethodField()
    comments_details = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'author', 'type', 'title', 'content', 'created_at', 'edit_at', 'end_at', 'add_vote', 'locked', 'comments_details', 'votes_details', 'votes_values']
        extra_kwargs = {'id': {'read_only': True},
                        'created_at': {'read_only': True},
                        'edit_at': {'read_only': True},
                        'end_at': {'allow_null': True},
                        'comments': {'read_only': True},
                        'votes_values': {'write_only': True},
                        }

    def update(self, instance, validated_data):
        for field in validated_data:
            setattr(instance, field, validated_data.get(field))
        instance.save()
        return instance

    def get_votes_details(self, obj):

        votes_details = []

        for vote_value in obj.votes_values.all():
            votes_details.append({vote_value.value: obj.votes.filter(vote__value__value=vote_value.value).count()})

        return votes_details

    def get_comments_details(self, obj):
        pass



class ListDocumentSerializer(serializers.ModelSerializer):

    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'author', 'type', 'title', 'content', 'created_at', 'edit_at', 'end_at', 'add_vote', 'comments_count', 'locked', 'votes']
        extra_kwargs = {'id': {'read_only': True},
                        'created_at': {'read_only': True},
                        'edit_at': {'read_only': True},
                        'comments': {'read_only': True},
                        'votes': {'read_only': True},
                        }

    def get_comments_count(self, obj):
        return obj.comments.all().count()
