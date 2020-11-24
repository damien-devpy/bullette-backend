from django.urls import path, include
from .views import RegistrationView

urlpatterns = [
    path('signup/', RegistrationView.as_view(), name='signup'),
]