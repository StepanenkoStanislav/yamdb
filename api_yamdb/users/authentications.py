from django.conf import settings
import jwt
from django.contrib.auth import get_user_model
from rest_framework import HTTP_HEADER_ENCODING, authentication
from rest_framework import exceptions, status

AUTH_HEADER_TYPES = ('Bearer',)
AUTH_HEADER_NAME = 'HTTP_AUTHORIZATION'
AUTH_HEADER_TYPE_BYTES = set(
    h.encode(HTTP_HEADER_ENCODING) for h in AUTH_HEADER_TYPES
)


class JWTAuth(authentication.BaseAuthentication):
    www_authenticate_realm = 'api'
    media_type = 'application/json'

    def authenticate(self, request):
        header = request.META.get(AUTH_HEADER_NAME)
        if header is None:
            return None

        if isinstance(header, str):
            header = header.encode(HTTP_HEADER_ENCODING)

        raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        valid_token = self.get_valid_token(raw_token)

        return self.get_user(valid_token), valid_token

    def authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def get_raw_token(self, header):
        parts = header.split()

        if len(parts) == 0:
            return None

        if parts[0] not in AUTH_HEADER_TYPE_BYTES:
            return None

        if len(parts) != 2:
            raise exceptions.AuthenticationFailed(
                'Authorization header must contain two space-delimited values',
                code=status.HTTP_401_UNAUTHORIZED,
            )

        return parts[1]

    def get_valid_token(self, raw_token):
        return jwt.decode(raw_token, settings.SECRET_KEY, 'HS256')

    def get_user(self, valid_token):
        if 'user_id' not in valid_token:
            raise exceptions.AuthenticationFailed(
                'Token contained no recognizable user identification',
                code=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            user = get_user_model().objects.get(id=valid_token['user_id'])
        except get_user_model().DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'User not found',
                code=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                'User is inactive', code=status.HTTP_401_UNAUTHORIZED
            )

        return user
