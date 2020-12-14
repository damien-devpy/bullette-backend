from .models import Comment, Vote, VoteValue
from rest_framework import serializers

class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['content']

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'author': {'read_only': True}}

    def update(self, instance, validated_data):

        for field in validated_data:
            setattr(instance, field, validated_data.get(field))
        instance.save()
        return instance

class CreateVoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['value']