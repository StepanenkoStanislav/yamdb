from django.contrib import admin

from reviews.models import Comment, Review


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text', 'score', 'pub_date')
    search_fields = ('text', 'author',)
    list_filter = ('score', 'author', 'pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'text', 'author', 'pub_date',)
    search_fields = ('review', 'text', 'author', 'pub_date',)
