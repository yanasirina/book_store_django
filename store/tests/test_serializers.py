from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from store.models import Book, UserBookRelation, User
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.book1 = Book.objects.create(name='Test Book 1', price=100.10)
        self.book2 = Book.objects.create(name='Test Book 2', price=10)
        self.user1 = User.objects.create(username="username1")
        self.user2 = User.objects.create(username="username2")

    def test_ok(self):
        books = Book.objects.all().annotate(
            bookmarks_count=Count(Case(When(userbookrelation__in_bookmarks=True, then=1))),
            rating=Avg('userbookrelation__rating')
        ).order_by('id')
        serializer_data = BookSerializer(books, many=True).data
        formatted_serializer_data = [dict(element) for element in serializer_data]

        expected_data = [
            {
                'id': self.book1.id,
                'likes_count': 0,
                'bookmarks_count': 0,
                'rating': None,
                'name': 'Test Book 1',
                'price': '100.10',
                'author_name': None,
            },
            {
                'id': self.book2.id,
                'likes_count': 0,
                'bookmarks_count': 0,
                'rating': None,
                'name': 'Test Book 2',
                'price': '10.00',
                'author_name': None,
            }
        ]

        self.assertEqual(expected_data, formatted_serializer_data)

    def test_likes_count(self):
        UserBookRelation.objects.create(user=self.user1, book=self.book1)
        UserBookRelation.objects.create(user=self.user1, book=self.book2, like=True)
        UserBookRelation.objects.create(user=self.user2, book=self.book2, like=True)

        books = Book.objects.all().annotate(
            bookmarks_count=Count(Case(When(userbookrelation__in_bookmarks=True, then=1))),
            rating=Avg('userbookrelation__rating')
        ).order_by('id')
        serializer_data = BookSerializer(books, many=True).data
        formatted_serializer_data = [dict(element) for element in serializer_data]
        expected_data = [
            {
                'id': self.book1.id,
                'likes_count': 0,
                'bookmarks_count': 0,
                'rating': None,
                'name': 'Test Book 1',
                'price': '100.10',
                'author_name': None,
            },
            {
                'id': self.book2.id,
                'likes_count': 2,
                'bookmarks_count': 0,
                'rating': None,
                'name': 'Test Book 2',
                'price': '10.00',
                'author_name': None,
            }
        ]

        self.assertEqual(expected_data, formatted_serializer_data)

    def test_bookmarks_count(self):
        UserBookRelation.objects.create(user=self.user1, book=self.book1)
        UserBookRelation.objects.create(user=self.user1, book=self.book2, in_bookmarks=True)
        UserBookRelation.objects.create(user=self.user2, book=self.book2, in_bookmarks=True)

        books = Book.objects.all().annotate(
            bookmarks_count=Count(Case(When(userbookrelation__in_bookmarks=True, then=1))),
            rating=Avg('userbookrelation__rating')
        ).order_by('id')
        serializer_data = BookSerializer(books, many=True).data
        formatted_serializer_data = [dict(element) for element in serializer_data]
        expected_data = [
            {
                'id': self.book1.id,
                'likes_count': 0,
                'bookmarks_count': 0,
                'rating': None,
                'name': 'Test Book 1',
                'price': '100.10',
                'author_name': None,
            },
            {
                'id': self.book2.id,
                'likes_count': 0,
                'bookmarks_count': 2,
                'rating': None,
                'name': 'Test Book 2',
                'price': '10.00',
                'author_name': None,
            }
        ]

        self.assertEqual(expected_data, formatted_serializer_data)

    def test_rating(self):
        UserBookRelation.objects.create(user=self.user1, book=self.book1, rating=1)
        UserBookRelation.objects.create(user=self.user1, book=self.book2, rating=5)
        UserBookRelation.objects.create(user=self.user2, book=self.book2, rating=4)

        books = Book.objects.all().annotate(
            bookmarks_count=Count(Case(When(userbookrelation__in_bookmarks=True, then=1))),
            rating=Avg('userbookrelation__rating')
        ).order_by('id')
        serializer_data = BookSerializer(books, many=True).data
        formatted_serializer_data = [dict(element) for element in serializer_data]
        expected_data = [
            {
                'id': self.book1.id,
                'likes_count': 0,
                'bookmarks_count': 0,
                'rating': '1.00',
                'name': 'Test Book 1',
                'price': '100.10',
                'author_name': None,
            },
            {
                'id': self.book2.id,
                'likes_count': 0,
                'bookmarks_count': 0,
                'rating': '4.50',
                'name': 'Test Book 2',
                'price': '10.00',
                'author_name': None,
            }
        ]

        self.assertEqual(expected_data, formatted_serializer_data)
