from django.contrib import admin

from . import models


@admin.register(models.Book)
class Book(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name', )
    ordering = ('price', )
