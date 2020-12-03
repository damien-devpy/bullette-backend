from django.urls import path, include
from .views import RegistrationView, UpdateUserView, DeleteUserView

urlpatterns = [
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('update_password/', UpdateUserView.as_view(), name='update-password'),
    path('delete_account/', DeleteUserView.as_view(), name='delete-user'),
]