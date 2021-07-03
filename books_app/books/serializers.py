from core.models import Book, BookGender
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    """Serializer for tags objects"""
    score = serializers.IntegerField(min_value=1, max_value=10,
                                     required=False, allow_null=True)
    author = serializers.CharField(max_length=255, required=True)
    num_pages = serializers.IntegerField(min_value=1)
    gender = serializers.PrimaryKeyRelatedField(
        required=False,
        many=False,
        queryset=BookGender.objects.all(),
    )

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'num_pages', 'status', 'score',
                  'user', 'gender')
        read_only_fields = ('id', 'user')


class BookGenderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=2)

    class Meta:
        model = BookGender
        fields = ('id', 'name')
        read_only_fields = ('id',)
