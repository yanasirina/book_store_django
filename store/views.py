from rest_framework.viewsets import ModelViewSet

from . import models
from . import serializers


class BookViewSet(ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
