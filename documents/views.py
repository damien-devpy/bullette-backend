from rest_framework import generics
from .models import Document
from .serializers import CreateOrUpdateDocumentSerializer, GetDocumentSerializer, GetDetailDocumentSerializer
from .permissions import IsAdminOrReadOnly
import pdb

class ListDocumentView(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = GetDocumentSerializer

class GetUpdateDeleteDocumentView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Document.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetDetailDocumentSerializer
        return CreateOrUpdateDocumentSerializer

class CreateDocumentView(generics.CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Document.objects.all()
    serializer_class = CreateOrUpdateDocumentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

