from django.db.models import Count, Case, When, Avg, F
from django.http import HttpResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from . import models
from . import serializers
from .permissions import IsOwnerOrStaffOrReadOnly


class BookViewSet(ModelViewSet):
    queryset = models.Book.objects.all().annotate(
            bookmarks_count=Count(Case(When(userbookrelation__in_bookmarks=True, then=1))),
            rating=Avg('userbookrelation__rating'),
            price_with_discount=F("price") - F("discount"),
        ).select_related('owner').prefetch_related('readers').order_by('id')
    serializer_class = serializers.BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filterset_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_fields = ['price']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    queryset = models.UserBookRelation.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        current_user = self.request.user
        if current_user:
            obj, _ = models.UserBookRelation.objects.get_or_create(user=current_user, book_id=self.kwargs['book'])
            return obj
        return HttpResponse('Unauthorized', status=401)


def auth(request):
    return render(request, 'store/oauth.html')
