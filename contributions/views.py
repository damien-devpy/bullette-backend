from rest_framework import generics
from .serializers import CreateCommentSerializer, CreateVoteSerializer
from .models import Comment, Vote
from documents.models import Document
from .permissions import IsAuthenticated
import pdb


class CreateCommentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer

    def perform_create(self, serializer):
        document = Document.documents.get_document_by_id(self.kwargs.get('pk'))
        serializer.save(author=self.request.user,
                        document=document,
                        )

class CreateVoteView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = CreateVoteSerializer

    def perform_create(self, serializer):
        document = Document.documents.get_document_by_id(self.kwargs.get('pk'))
        serializer.save(author=self.request.user,
                        document=document,
                        )

