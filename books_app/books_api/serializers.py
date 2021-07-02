from rest_framework import serializers

from core.models import Book, BookGender


class BookSerializer(serializers.ModelSerializer):
    """Serializer for tags objects"""
    score = serializers.IntegerField(min_value=1, max_value=10)
    class Meta:
        model = Book
        fields = ('id', 'title', 'num_pages', 'status', 'score', 'user')
        read_only_fields = ('id', 'user')


class BookGenderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=2)

    class Meta:
        model = BookGender
        fields = ('id', 'name')
        read_only_fields = ('id',)