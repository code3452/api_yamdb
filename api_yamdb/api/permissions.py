from rest_framework import permissions

from users.models import ADMIN, MODERATOR


class IsAdminSuperuser(permissions.BasePermission):
    """Права доступа админу и суперпользователю."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == ADMIN
                or request.user.is_superuser)


class IsAdmin(permissions.BasePermission):
    """Права доступа админу."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.role == ADMIN
        )


class IsAuthorModeratorAdminSuperuserOrReadOnly(permissions.BasePermission):
    """Права доступа админу, суперпользователю, модератору, автору."""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == ADMIN
                or request.user.role == MODERATOR
                or obj.author == request.user
                or request.user.is_superuser)


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
