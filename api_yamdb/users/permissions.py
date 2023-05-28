from rest_framework import permissions


class SuperUserOrAdminOnly(permissions.BasePermission):
    '''Docsting'''
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )


class AuthUserOnly(permissions.BasePermission):
    '''Docsting'''
    # Use with IsAuthenticated permission
    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'user'
            and obj.author == request.user
            or request.method in permissions.SAFE_METHODS
        )


class ModeratorOnly(permissions.BasePermission):
    '''Docsting'''
    # Use with IsAuthenticated permission
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'moderator'
