from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Book
from books_api import serializers
from books_api.permissions import ManageOwnBooks


class BooksViewset(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all()
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, ManageOwnBooks)

    def get_queryset(self):
        """Retrieve the books for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new book"""
        serializer.save(user=self.request.user)
