from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book1 = Book.objects.create(name='Test Book 1', price=100.10)
        book2 = Book.objects.create(name='Test Book 2', price=10)

        serializer_data = BookSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'Test Book 1',
                'price': '100.10'
            },
            {
                'id': book2.id,
                'name': 'Test Book 2',
                'price': '10.00'
            }
        ]

        self.assertEqual(expected_data, serializer_data)
