from django.urls import path

from .views import DeleteUserView, RegistrationView, UpdateUserView

urlpatterns = [
    path("signup/", RegistrationView.as_view(), name="signup"),
    path("update_user/", UpdateUserView.as_view(), name="update-user"),
    path("delete_account/", DeleteUserView.as_view(), name="delete-user"),
]
