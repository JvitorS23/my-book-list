from books import serializers
from books.permissions import ManageOwnBooks, IsSuperUser
from core.models import Book, BookGender
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class BooksViewset(viewsets.ModelViewSet):
    """Manage books in the database"""
    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all()
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, ManageOwnBooks)

    def get_queryset(self):
        """Retrieve the books for the authenticated user"""
        queryset = self.queryset.filter(user=self.request.user)

        status = self.request.query_params.get('status', 'ALL')
        if status != 'ALL':
            queryset = queryset.filter(status=status)

        gender_id = self.request.query_params.get('gender', 'ALL')
        if gender_id != 'ALL':
            queryset = queryset.filter(gender_id=gender_id)

        return queryset

    def create(self, request, *args, **kwargs):
        """Manage creating book for user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        exists = self.queryset.filter(user=self.request.user).filter(
            title=serializer.validated_data['title']).exists()
        if exists:
            return Response('You already have a book with this title',
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class BookGenderViewSet(viewsets.ModelViewSet):
    """Book gender viewset"""
    serializer_class = serializers.BookGenderSerializer
    queryset = BookGender.objects.all()
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperUser)
