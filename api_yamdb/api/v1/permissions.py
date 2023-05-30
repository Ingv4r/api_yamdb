from rest_framework import permissions
from rest_framework.permissions import BasePermission


class SuperUserOrAdminOnly(permissions.BasePermission):
    """Доступ только для superuser или админ."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class SuperUserOrAdminCreateOnly(permissions.BasePermission):
    """Доутуп к объекту только у superuser и админа."""
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.is_superuser


class AuthorOrStuffOnly(permissions.BasePermission):
    """Доступ к объекту у автора объекта и администрации."""
    def has_object_permission(self, request, view, obj):

        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.is_superuser
                or request.user.is_admin
                or request.user.is_moderator
            )
        )


class IsAdminUserOrReadOnly(BasePermission):
    """Доступ для чтения или администратора и superuser."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )
