from django.urls import path

from .views import (
    CreateDocumentView,
    GetUpdateDeleteDocumentView,
    ListDocumentView,
)

urlpatterns = [
    path("", ListDocumentView.as_view(), name="list-document"),
    path(
        "create_document/",
        CreateDocumentView.as_view(),
        name="create-document",
    ),
    path(
        "documents/<int:pk>",
        GetUpdateDeleteDocumentView.as_view(),
        name="get-update-delete-document",
    ),
]
