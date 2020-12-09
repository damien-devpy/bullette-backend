from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from .models import Document
from .serializers import DocumentSerializer, ListDocumentSerializer
from .permissions import IsAdmin

class CreateDocumentView(generics.CreateAPIView):
    permission_classes = [IsAdmin, IsAuthenticated]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ListDocumentView(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = ListDocumentSerializer