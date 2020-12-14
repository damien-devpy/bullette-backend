from rest_framework import generics

from documents.models import Document

from .models import Comment, Vote
from .permissions import IsAuthenticated
from .serializers import CreateOrUpdateCommentSerializer, CreateVoteSerializer


class CreateCommentView(generics.CreateAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Comment.objects.all()
    serializer_class = CreateOrUpdateCommentSerializer

    def perform_create(self, serializer):
        document = Document.documents.get_document_by_id(self.kwargs.get("pk"))
        serializer.save(
            author=self.request.user,
            document=document,
        )


class CreateVoteView(generics.CreateAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Vote.objects.all()
    serializer_class = CreateVoteSerializer

    def perform_create(self, serializer):
        document = Document.documents.get_document_by_id(self.kwargs.get("pk"))
        serializer.save(
            author=self.request.user,
            document=document,
        )
