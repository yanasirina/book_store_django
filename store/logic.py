from django.db.models import Avg

from store import models


def set_rating(book):
    rating = models.UserBookRelation.objects.filter(book=book).aggregate(rating=Avg('rating')).get('rating')
    book.rating = rating
    book.save()
