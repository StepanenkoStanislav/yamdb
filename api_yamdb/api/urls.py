from django.urls.conf import path, include
from rest_framework.routers import SimpleRouter

from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    CommentViewSet,
    ReviewViewSet,
    get_token,
    UserViewSet,
    UserSignupSet,
)

router_v1 = SimpleRouter()
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>[^/.]+)/reviews', ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comments',
)
router_v1.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', UserSignupSet.as_view({'post': 'create'})),
    path('v1/auth/token/', get_token),
]
