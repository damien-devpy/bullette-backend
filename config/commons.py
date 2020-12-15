from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def get_client_with_auth(user):
    client = APIClient()
    token = get_tokens(user)
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])
    return client
