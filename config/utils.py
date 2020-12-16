from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework.views import exception_handler
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def get_client_with_auth(user):
    client = APIClient()
    token = get_tokens(user)
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])
    return client


def custom_exception_handler(exception, context):
    response = exception_handler(exception, context)

    # If error 500 occured
    if response is None:
        # Handle it properly with context data and exception
        return Response(
            {
                "view": str(context["view"]),
                "request": str(context["request"]),
                "error": str(exception),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Otherwise do nothing and let DRF manage it
    return response
