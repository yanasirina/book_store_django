from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book1 = Book.objects.create(name='Test Book 1', price=100.10)
        book2 = Book.objects.create(name='Test Book 2', price=10)

        serializer_data = BookSerializer([book1, book2], many=True).data
        formatted_serializer_data = [dict(element) for element in serializer_data]
        expected_data = [
            {
                'id': book1.id,
                'name': 'Test Book 1',
                'price': '100.10',
                'author_name': None
            },
            {
                'id': book2.id,
                'name': 'Test Book 2',
                'price': '10.00',
                'author_name': None
            }
        ]

        self.assertEqual(expected_data, formatted_serializer_data)
