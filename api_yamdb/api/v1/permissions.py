from rest_framework import permissions
from rest_framework.permissions import BasePermission


class SuperUserOrAdminOnly(permissions.BasePermission):
    """Docsting"""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
            or request.user.is_superuser
        )


class SuperUserOrAdminCreateOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == "admin" or request.user.is_superuser


class AuthorOrStuffOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.is_superuser
                or request.user.role == "admin"
                or request.user.role == "moderator"
            )
        )


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == "admin"
        )
