from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.db.models import Q

from store.models import Book
from store.serializers import BookSerializer


class BookApiTestCase(APITestCase):
    def setUp(self):
        self.book1 = Book.objects.create(name='Book', price=100.50)
        self.book3 = Book.objects.create(name='Book 2', price=325, author_name='testing Author')
        self.book2 = Book.objects.create(name='Test Book', price=100.50, author_name='Author')

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        qs = Book.objects.all()
        serializer_data = BookSerializer(qs, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 100.50})
        qs = Book.objects.filter(price=100.50)
        serializer_data = BookSerializer(qs, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer_data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'test'})
        qs = Book.objects.filter(Q(name__icontains='test') | Q(author_name__icontains='test'))
        serializer_data = BookSerializer(qs, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer_data)

    def test_get_order(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'price'})
        qs = Book.objects.all().order_by('price')
        serializer_data = BookSerializer(qs, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer_data)

        response = self.client.get(url, data={'ordering': '-price'})
        qs = Book.objects.all().order_by('-price')
        serializer_data = BookSerializer(qs, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer_data)
