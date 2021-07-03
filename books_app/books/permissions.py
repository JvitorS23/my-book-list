from rest_framework import permissions


class ManageOwnBooks(permissions.BasePermission):
    """Allow user to manage their own books"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own book"""
        return obj.user == request.user


class IsSuperUser(permissions.BasePermission):
    """Allow only super user to create/edit book genders"""

    def has_permission(self, request, view):
        """Allow only super user to edit book genders"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_superuser)
