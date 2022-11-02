from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from . import models
from . import serializers


class BookViewSet(ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['price']
    search_fields = ['name', 'author_name']
