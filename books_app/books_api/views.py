from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        """Manage creating book for user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        exists = self.queryset.filter(user=self.request.user).filter(
            title=serializer.data['title']).exists()
        if exists:
            return Response('You already have a book with this title',
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
