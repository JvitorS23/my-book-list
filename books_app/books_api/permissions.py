from rest_framework import permissions


class ManageOwnBooks(permissions.BasePermission):
    """Allow user to manage their own books"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        return obj.user == request.user
