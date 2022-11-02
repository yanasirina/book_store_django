from django.db import models


class Book(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2)
    author_name = models.CharField(verbose_name='Имя Автора', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Список Книг"

    def __str__(self):
        return f'ID {self.id}: {self.name}'

