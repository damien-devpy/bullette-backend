from django.urls import path

from .views import CreateCommentView, CreateVoteView

urlpatterns = [
    path(
        "<int:pk>/comment/", CreateCommentView.as_view(), name="create-comment"
    ),
    path("<int:pk>/vote/", CreateVoteView.as_view(), name="create-vote"),
]
