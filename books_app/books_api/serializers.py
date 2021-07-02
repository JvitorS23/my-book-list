from rest_framework import serializers

from core.models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for tags objects"""
    score = serializers.IntegerField(min_value=1, max_value=10)
    class Meta:
        model = Book
        fields = ('id', 'title', 'num_pages', 'status', 'score', 'user')
        read_only_fields = ('id', 'user')
