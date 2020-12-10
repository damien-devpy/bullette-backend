from rest_framework import generics
from .models import Document
from .serializers import DocumentSerializer, ListDocumentSerializer
from .permissions import IsAdminOrReadOnly


class ListDocumentView(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = ListDocumentSerializer

class GetUpdateDeleteDocumentView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class CreateDocumentView(generics.CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

