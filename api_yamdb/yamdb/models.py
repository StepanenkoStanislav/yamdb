from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
        help_text='Введите название категории',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Ссылка',
        help_text='Введите ссылку',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return (
            self.name[: settings.MAX_PRESENTATION_LENGTH] + '...'
            if len(self.name) > settings.MAX_PRESENTATION_LENGTH
            else self.name
        )


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
        help_text='Введите название жанра',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Ссылка',
        help_text='Введите ссылку',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return (
            self.name[: settings.MAX_PRESENTATION_LENGTH] + '...'
            if len(self.name) > settings.MAX_PRESENTATION_LENGTH
            else self.name
        )


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
        help_text='Введите название произведения',
    )
    year = models.IntegerField(
        verbose_name='Год выпуска', help_text='Введите год выпуска'
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        help_text='Введите рейтинг произведения',
        null=True,
        default=None,
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
        help_text='Введите описание',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Укажите жанры',
    )
    category = models.ForeignKey(
        Category,
        default=None,
        on_delete=models.SET_DEFAULT,
        related_name='titles',
        verbose_name='Категория',
        help_text='Выберите категорию',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return (
            self.name[: settings.MAX_PRESENTATION_LENGTH] + '...'
            if len(self.name) > settings.MAX_PRESENTATION_LENGTH
            else self.name
        )
