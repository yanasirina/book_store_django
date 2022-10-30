from rest_framework.serializers import ModelSerializer

from . import models


class BookSerializer(ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'
