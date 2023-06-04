import json

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.db.models import Q, Count, Case, When, Avg, F

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


User = get_user_model()


class BookApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_username")
        self.book1 = Book.objects.create(name='Book', price=100.50, owner=self.user)
        self.book3 = Book.objects.create(name='Book 2', price=325, author_name='testing Author')
        self.book2 = Book.objects.create(name='Test Book', price=100.50, author_name='Author')

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        qs = Book.objects.all().annotate(
            bookmarks_count=Count(Case(When(userbookrelation__in_bookmarks=True, then=1))),
            price_with_discount=F("price") - F("discount"),
        ).order_by('id')
        serializer_data = BookSerializer(qs, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 100.50})
        qs = Book.objects.filter(price=100.50).annotate(
            bookmarks_count=Count(Case(When(userbookrelation__in_bookmarks=True, then=1))),
            price_with_discount=F("price") - F("discount"),
        ).order_by('id')
        serializer_data = BookSerializer(qs, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer_data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'test'})
        qs = Book.objects.filter(Q(name__icontains='test') | Q(author_name__icontains='test')).annotate(
            bookmarks_count=Count(Case(When(userbookrelation__in_bookmarks=True, then=1))),
            price_with_discount=F("price") - F("discount"),
        ).order_by('id')
        serializer_data = BookSerializer(qs, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer_data)

    def test_get_ordering(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'price'})
        qs = Book.objects.all().annotate(
            bookmarks_count=Count(Case(When(userbookrelation__in_bookmarks=True, then=1))),
            price_with_discount=F("price") - F("discount"),
        ).order_by('price')
        serializer_data = BookSerializer(qs, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer_data)

        response = self.client.get(url, data={'ordering': '-price'})
        qs = Book.objects.all().annotate(
            bookmarks_count=Count(Case(When(userbookrelation__in_bookmarks=True, then=1))),
            price_with_discount=F("price") - F("discount"),
        ).order_by('-price')
        serializer_data = BookSerializer(qs, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer_data)

    def test_create_unauthorized(self):
        url = reverse('book-list')
        data = {
            "name": "test name",
            "price": 100
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create(self):
        books_count_before = Book.objects.all().count()
        url = reverse('book-list')
        data = {
            "name": "test name",
            "price": 100
        }
        json_data = json.dumps(data)

        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type="application/json")
        books_count_after = Book.objects.all().count()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(books_count_after, books_count_before + 1)
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book1.id, ))
        data = {
            "name": self.book1.name,
            "price": 150,
            "author_name": "author"
        }
        json_data = json.dumps(data)

        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.book1.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.book1.name, data['name'])
        self.assertEqual(self.book1.price, data['price'])
        self.assertEqual(self.book1.author_name, data['author_name'])

    def test_update_another_owner(self):
        url = reverse('book-detail', args=(self.book2.id, ))
        data = {
            "name": self.book2.name,
            "price": 150,
            "author_name": "author"
        }
        json_data = json.dumps(data)

        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_update_staff(self):
        staff_user = User.objects.create(username="staff", is_staff=True)
        url = reverse('book-detail', args=(self.book2.id, ))
        data = {
            "name": self.book2.name,
            "price": 150,
            "author_name": "author"
        }
        json_data = json.dumps(data)

        self.client.force_login(staff_user)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class BookRelationTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="test_username")
        self.user2 = User.objects.create(username="test_username2")
        self.book1 = Book.objects.create(name='Book', price=100.50, owner=self.user1)
        self.book2 = Book.objects.create(name='Test Book', price=100.50, author_name='Author')

    def test_reactions(self):
        url = reverse('userbookrelation-detail', args=(self.book1.id, ))

        data = {
            "like": True,
        }
        json_data = json.dumps(data)

        self.client.force_login(self.user2)
        response = self.client.patch(url, data=json_data, content_type="application/json")

        relation = UserBookRelation.objects.get(user=self.user2, book=self.book1)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(relation.like)
        self.assertFalse(relation.in_bookmarks)
