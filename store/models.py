from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Book(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2)
    discount = models.DecimalField(verbose_name='Скидка', max_digits=7, decimal_places=2, help_text='Скидка в рублях',
                                   default=0)
    author_name = models.CharField(verbose_name='Имя Автора', max_length=255, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owned_books')
    readers = models.ManyToManyField(User, through='UserBookRelation', related_name='books')

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Список Книг"

    def __str__(self):
        return f'ID {self.id}: {self.name}'


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Very bad'),
        (1, 'Bad'),
        (1, 'Ok'),
        (1, 'Good'),
        (1, 'Very good'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(choices=RATE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}: {self.book}, {self.rating}'
