from django.contrib import admin

from yamdb.models import Category, Genre, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'rating', 'description', 'category')
    list_filter = (
        'rating',
        'category',
        'year',
    )
    search_fields = (
        'name',
        'description',
    )
