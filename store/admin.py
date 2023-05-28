from django.contrib import admin

from . import models


@admin.register(models.Book)
class Book(admin.ModelAdmin):
    list_display = ('name', 'author_name', 'price')
    search_fields = ('name', 'author_name')
    ordering = ('price', )


@admin.register(models.UserBookRelation)
class Book(admin.ModelAdmin):
    pass
