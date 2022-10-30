from django.db import models


class Book(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Список Книг"

    def __str__(self):
        return self.name

