from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from yamdb.models import Title, User


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка произведения',
        help_text='Укажите оценку произведения (от 1 до 10)',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Выберите произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
        help_text='Укажите автора отзыва',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва',
        help_text='Введите дату отзыва',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('title', 'author')

    def __str__(self):
        return (
            self.text[: settings.MAX_PRESENTATION_LENGTH] + '...'
            if len(self.text) > settings.MAX_PRESENTATION_LENGTH
            else self.text
        )

    def clean_score(self):
        if self.score < 1 or self.score > 10:
            raise ValidationError('Оценка должна быть в диапазоне от 1 до 10')


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите комментарий к отзову',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Выберите отзыв',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Выберите автора',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария',
        help_text='Введите дату комментария',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return (
            self.text[: settings.MAX_PRESENTATION_LENGTH] + '...'
            if len(self.text) > settings.MAX_PRESENTATION_LENGTH
            else self.text
        )
