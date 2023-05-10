import datetime

import django_filters
from django.core.signing import BadSignature
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
import jwt
from rest_framework import (
    filters,
    mixins,
    pagination,
    permissions,
    status,
    viewsets,
)
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.apps import signal_need_update_rating, signal_user_registered
from api.permissions import (
    IsAdminOnly,
    IsAdminOrReadOnly,
    IsAdminModeratorAuthorOrReadOnly,
)
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleListSerializer,
    CommentSerializer,
    ReviewSerializer,
    CustomUserSerializer,
)
from api.utilites import signer
from yamdb.models import (
    Category,
    Genre,
    Title,
)
from reviews.models import Review
from users.models import CustomUser


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    genre = django_filters.CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'year', 'name']


class ListCreateDestroyViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleListSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    filterset_fields = ('author', 'title')
    search_fields = ('text',)

    lookup_field = 'id'

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'),
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )

        signal_need_update_rating.send(
            ReviewViewSet, title_id=self.kwargs.get('title_id')
        )

    def perform_update(self, serializer):
        serializer.save()

        signal_need_update_rating.send(
            ReviewViewSet, title_id=self.kwargs.get('title_id')
        )

    def perform_destroy(self, instance):
        instance.delete()

        signal_need_update_rating.send(
            ReviewViewSet, title_id=self.kwargs.get('title_id')
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    filterset_fields = ('author', 'review')
    search_fields = ('text',)

    lookup_field = 'id'

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'),
        )
        serializer.save(
            author=self.request.user,
            review=review,
        )


# ====================================
class UserViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'email')

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+)',
    )
    def get_user_by_username(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def get_me_data(self, request):
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                request.user,
                data=request.data,
                partial=True,
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSignupSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            self.perform_create(serializer)
            user = serializer.instance
            user_status = status.HTTP_200_OK
        else:
            is_user_exists = getattr(serializer, 'is_user_exists', None)
            is_email_exists = getattr(serializer, 'is_email_exists', None)

            if ((is_user_exists is None or is_email_exists is None)
                    or not (is_user_exists and is_email_exists)):
                raise ValidationError(serializer.errors)

            user = self.queryset.get(
                username=request.data.get('username', ''),
                email=request.data.get('email', ''),
            )
            user_status = status.HTTP_200_OK

        headers = self.get_success_headers(serializer.data)
        signal_user_registered.send(UserSignupSet, instance=user)

        return Response(
            {
                'email': request.data['email'],
                'username': request.data['username'],
            },
            status=user_status,
            headers=headers,
        )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_token(request):
    user_name = request.data.get('username', None)
    if user_name is None:
        return Response(
            {'username': 'Отсутствует обязательное поле'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    confirmation_code = request.data.get('confirmation_code', None)
    if confirmation_code is None:
        return Response(
            {'confirmation_code': 'Отсутствует обязательное поле'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = get_object_or_404(CustomUser, username=user_name)

    try:
        check_code = signer.unsign(confirmation_code)
    except BadSignature:
        return Response(
            {'confirmation_code': 'Некорректный confirmation_code'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if check_code != user_name:
        return Response(
            {'confirmation_code': 'Некорректный confirmation_code'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    exp_date = datetime.datetime.now() + datetime.timedelta(days=5)
    unix_time = exp_date.timestamp()
    token = {
        "token_type": "access",
        "exp": str(int(unix_time)),
        "user_id": user.id,
    }

    jwt_token = jwt.encode(token, settings.SECRET_KEY, "HS256")
    return Response({'token': jwt_token}, status=status.HTTP_200_OK)
