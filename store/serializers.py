from rest_framework import serializers

from . import models


class BookReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name')


class BookSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    bookmarks_count = serializers.IntegerField(read_only=True)    # используем аннотацию
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    price_with_discount = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(source='owner.username', default='', read_only=True)
    readers = BookReaderSerializer(many=True, read_only=True)

    class Meta:
        model = models.Book
        fields = ('id', 'name', 'price', 'author_name', 'likes_count', 'bookmarks_count', 'rating',
                  'price_with_discount', 'owner_name', 'readers')

    def get_likes_count(self, instance):
        likes_count = models.UserBookRelation.objects.filter(book=instance, like=True).count()
        return likes_count


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rating')
