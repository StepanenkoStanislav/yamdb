from datetime import datetime

from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator

from api.utilites import CurrentTitleDefault
from users.models import CustomUser
from yamdb.models import Category, Genre, Title
from reviews.models import Comment, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'

    def validate_slug(self, slug):
        slug = slug.lower()
        if Category.objects.filter(slug=slug).exists():
            raise exceptions.ValidationError(f'Cсылка {slug} уже существует.')
        return slug


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'

    def validate_slug(self, slug):
        slug = slug.lower()
        if Genre.objects.filter(slug=slug).exists():
            raise exceptions.ValidationError(f'Жанр {slug} уже существует.')
        return slug


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug', required=True
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug',
        required=True,
    )
    rating = serializers.ReadOnlyField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def validate_year(self, year):
        if not 0 <= year <= datetime.now().year:
            raise exceptions.ValidationError('Введите корректный год.')
        return year


class TitleListSerializer(TitleSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    title = serializers.HiddenField(
        default=CurrentTitleDefault()
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='Один пользователь - одно ревью',
            ),
        ]

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                'Оценка должна быть в диапазоне от 1 до 10'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


# ===============================================
# Users
# ===============================================
class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[]
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Username can not be "me".')
        self.is_user_exists = CustomUser.objects.filter(
            username=value
        ).exists()
        if self.is_user_exists:
            raise serializers.ValidationError(
                f'User with username "{value}" exists'
            )
        return value

    def validate_email(self, value):
        self.is_email_exists = CustomUser.objects.filter(
            email=value
        ).exists()
        if self.is_email_exists:
            raise serializers.ValidationError(
                f'User with email "{value}" exists'
            )
        return value
