from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import get_tokens

from .serializers import CreateOrUpdateUserSerializer


class RegistrationView(APIView):
    """Allow user to signup to the plateform."""

    def post(self, request):
        serializer = CreateOrUpdateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens(user)

            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    """Allow user to update his own information."""

    permission_classes = [
        IsAuthenticated,
    ]

    def patch(self, request):
        serializer = CreateOrUpdateUserSerializer(
            instance=request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    """Allow user to delete his own account."""

    permission_classes = [
        IsAuthenticated,
    ]

    def delete(self, request):
        user = get_user_model().objects.get(id=request.user.id)
        user.delete()
        return Response(status=status.HTTP_200_OK)
