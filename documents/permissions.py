from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    message = "Vous n'êtes pas autorisé à créer un document"
    code = "not_an_admin"

    def has_permission(self, request, view):

        return request.user.is_superuser